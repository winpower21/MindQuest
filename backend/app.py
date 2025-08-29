from flask import Flask
from flask_jwt_extended import JWTManager
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_cors import CORS
from flask_migrate import Migrate
from celery.schedules import crontab

from applications.auth import init_jwt
from applications.config import Config
from applications.models import User, Role, db
from applications.resources import api
from applications.extensions import whooshee
from applications.celery_init import celery_init_app
from applications.tasks import monthly_report

jwt = JWTManager()
migrate = Migrate()

def createApp():
    app =  Flask(__name__, template_folder="frontend", static_folder="frontend")
    app.config.from_object(Config)
    CORS(app)   
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    whooshee.init_app(app)
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app, datastore=datastore, register_blueprint=False) # type: ignore
    app.app_context().push()
    jwt.init_app(app)
    init_jwt(jwt)
    return app

app = createApp()
celery = celery_init_app(app)
celery.autodiscover_tasks()

with app.app_context():
    db.create_all()
    userdatastore : SQLAlchemyUserDatastore = app.security.datastore # type: ignore
    userdatastore.find_or_create_role(name="admin", description="Administrator")
    userdatastore.find_or_create_role(name="user", description="User")
    db.session.commit()
    created = False
    if not userdatastore.find_user(email="admin@mindquest.com"):
        userdatastore.create_user(name="Administrator", email="admin@mindquest.com", password=hash_password("admin"), roles=["admin"], avatar_seed=0, avatar_style="notionists")
        created = True
    if not userdatastore.find_user(email="user@mindquest.com"):
        userdatastore.create_user(name="User", email="user@mindquest.com", password=hash_password("user"), roles=["user"], avatar_seed=00, avatar_style="notionists")
        created = True
    db.session.commit()
    if created:
        whooshee.reindex()
    
@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/2'),
        monthly_report.s(),
    )
# crontab(minute='*/2'),


import applications.routes #noqa
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)