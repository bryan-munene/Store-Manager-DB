import os
from flask import Flask, Blueprint
from instance.config import app_config
from manage import DatabaseSetup

def create_app(config):
    '''This function configures the Flask app'''

    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config["TESTING"] = True
    app.secret_key = os.getenv('SECRET_KEY')
    
    url = os.getenv('DATABASE_URL')
    db = DatabaseSetup(url)

    db.create_tables()
    db.create_default_admin_user()

    return app
