from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_by_env

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_env[config_name])
    db.init_app(app)

    return app
