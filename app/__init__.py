import os
from flask import Flask, Blueprint
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from instance.config import app_config
from manage import DatabaseSetup
from app.api.v1.views.sales import sales_bp
from app.api.v1.views.items import items_bp
from app.api.v1.views.auth import users_bp
from app.api.v1.views.categories import categories_bp
blacklist = set()
jwt = JWTManager()

def create_app(config):
    '''This function configures the Flask app'''

    app = Flask(__name__, instance_relative_config=True)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config.from_pyfile('config.py')
    app.config['testing'] = True
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config["JWT_SECRET_KEY"]= os.getenv('SECRET_KEY')
    jwt.init_app(app)

    db = DatabaseSetup(config)
    
    db.create_tables()
    db.create_default_admin_user()

    app.register_blueprint(sales_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)


    return app

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist