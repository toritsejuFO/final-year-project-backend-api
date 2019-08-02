from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

from config import config_by_env

db = SQLAlchemy()

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

title = 'Biometric Attendance and Exam Vieirfication System'
description = 'Backend API for managing resources on the Biometric Attendance and Exam Vieirfication System'
api = Api(doc='/docs', version='1.0', title=title, description=description, authorizations=authorizations)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_env[config_name])
    db.init_app(app)
    api.init_app(app)

    return app
