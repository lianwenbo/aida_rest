import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import config
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bcrypt.init_app(app)
    # import the blueprint here is to keep the
    # initialization order
    from .views.auth import auth_blueprint
    from .views.question import question_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(question_blueprint)
    return app

