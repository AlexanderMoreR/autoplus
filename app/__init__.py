import os
from flask import Flask
from .loginFacebok import loginfacebook
from .createFacebook import createfacebook

from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(loginfacebook)
    app.register_blueprint(createfacebook)

    return app