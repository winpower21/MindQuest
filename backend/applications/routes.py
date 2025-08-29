from flask import current_app as app, send_from_directory
from flask import render_template, request, jsonify
from flask_security.decorators import auth_required, roles_required, roles_accepted
from flask_security.utils import verify_password, hash_password
from .models import db, User
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import login_user, logout_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .auth import token_blocklist


datastore : SQLAlchemyUserDatastore = app.security.datastore # type: ignore


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/login", methods=["POST"]) # type: ignore
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Invalid email or password"}), 400

    user = datastore.find_user(email=email)
    if not user or not verify_password(password=password, password_hash=user.password):  # type: ignore
        return jsonify({"message": "Invalid email or password"}), 400
    if user.active == False:
        return jsonify({"message": "Your account has been deactivated. Contact Administrator"}), 400
    login_user(user)

    # Create auth token
    authToken = create_access_token(identity=str(user.email))
    
    # Create user object
    user = {"email": user.email, "role" : user.roles[0].name, "id": user.id, "name": user.name, "avatar_seed":user.avatar_seed, "avatar_style":user.avatar_style}
    return jsonify({
        "authToken": authToken,
        "user": user,
    }), 200

@app.route("/api/check-password", methods=["POST"])
@jwt_required()
def check_password():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    data = request.get_json()
    existing_password = data.get("password")
    
    if not existing_password:
        return jsonify({"message":"Provide current password"}), 400
    if verify_password(existing_password, password_hash=user.password):
        return jsonify({"message":"Correct Password"}), 200
    else:
        return jsonify({"message":"Incorrect password"}), 400



@app.route("/api/reset-password", methods=["POST"])
@jwt_required()
def reset_password():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    data = request.get_json()
    new_password = data.get("password")
    if not new_password:
        return jsonify({"message":"Provide new password"}), 400
    user.password = hash_password(new_password)
    db.session.commit()
    return jsonify({"message":"Password has been reset"})


@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"message":"User not fouond"}), 404
    token = get_jwt()
    auth_jti = token['jti']
    token_blocklist.add(auth_jti)
    
    logout_user()
    return jsonify({"message": "Successfully Logged Out"}), 200


@app.route("/api/register", methods=["POST"]) # type: ignore
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    avatar_seed = data.get("avatar_seed")
    avatar_style = data.get("avatar_style")
    if not email or not name or not password:
        return jsonify({"message": "Invalid inputs"}), 400
    if not datastore.find_user(email=email):
        try:
            datastore.create_user(name=name, email=email, password=hash_password(password), roles = ["user"], avatar_seed = avatar_seed, avatar_style = avatar_style)
            db.session.commit()
            return jsonify({"message": "User created successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error creating user: {e}"}), 404
    else:
        return jsonify({"message": "Email already exists"}), 400

        
@app.route("/api/delete_account", methods=["POST"])# type: ignore
@jwt_required()
def delete_acc():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email = current_user_email).first()
    if not user:
        return jsonify({"message": "User does not exist"}), 400
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"User Deleted Successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":f"Error deleting user{e}"}), 404
        
@app.route("/api/user_activation", methods=["POST"]) # type: ignore
@jwt_required()
@roles_required("admin")
def update_user_status():
    data = request.get_json()
    id = data.get("id")
    user = datastore.find_user(id=id)
    if not user:
        return jsonify({"message":"User does not exist"}), 400
    else:
        try:
            datastore.toggle_active(user)
            db.session.commit()
            return jsonify({"message":f"User ({user.name}) status set to {user.active}"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":f"Unable to change user status: {str(e)}"}), 400
        
        


# Celery job triggers.
from celery.result import AsyncResult
from .tasks import generate_user_report, monthly_report, generate_msg, generate_user_attempt_report

@app.route("/api/export_csv")
@jwt_required()
def export():
    jwt = get_jwt_identity()
    user = User.query.filter_by(email=jwt).first()
    user_id = user.id
    result = generate_user_report.delay(user_id)
    return {
        "id": result.id
    }

@app.route("/api/export_attempt_csv/<int:subject_id>")
@jwt_required()
def export_attempt_report(subject_id):
    jwt = get_jwt_identity()
    user = User.query.filter_by(email=jwt).first()
    user_id = user.id
    user_role = user.roles[0].name
    result = generate_user_attempt_report.delay(subject_id,user_id, user_role)
    return {
        "id": result.id
    }
    
    
@app.route('/api/csv_result/<id>')
@jwt_required()
def csv_result(id):
    res = AsyncResult(id)
    filename = res.result    
    return send_from_directory('static', res.result, as_attachment=True, download_name=filename)





@app.route('/api/send_mail')
@jwt_required()
def send_mail():
    res = monthly_report.delay()
    return {
        "message": res.result
    }
