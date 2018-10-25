from flask import Flask, Blueprint

from instance.config import app_config


import os

def create_app(config):
    '''This function configures the Flask app'''

    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config])
    app.config["TESTING"] = True
    
    app.secret_key = os.urandom(12)


    return app
