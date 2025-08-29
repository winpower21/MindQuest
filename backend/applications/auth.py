from flask import jsonify
# Create a token blocklist set
token_blocklist = set()

def init_jwt(jwt):
    # Register the JWT token blocklist check function
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in token_blocklist
        
    # You can also add other JWT configurations here
    # For example:
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401