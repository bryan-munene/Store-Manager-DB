import os
from flask import Flask, Blueprint
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from instance.config import app_config
from manage import DatabaseSetup

jwt = JWTManager()

def create_app(config):
    '''This function configures the Flask app'''

    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config["TESTING"] = True
    app.secret_key = os.getenv('SECRET_KEY')
    
    app.config["JWT_SECRET_KEY"]= os.getenv('SECRET_KEY')
    jwt.init_app(app)

    url = os.getenv('DATABASE_URL')
    db = DatabaseSetup(url)


    db.create_tables(url)
    db.create_default_admin_user(url)

    from app.api.v1.views.auth import users_bp
    app.register_blueprint(users_bp)


    return app
