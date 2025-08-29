from datetime import timedelta
class Config():
    WHOOSHEE_DIR = 'whooshee_index'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "my_precious_two"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Token"
    SECRET_KEY = "secret_key"
    JWT_SECRET_KEY = "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_MAX_AGE = None  # Disable persistent sessions
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = False  # Ensure login requires valid token
    
