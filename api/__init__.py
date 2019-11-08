import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

from config import config_by_env
from logger import stream_logger, logger

db = SQLAlchemy()
mail = Mail()

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-auth-token'
    }
}

title = 'Biometric Attendance and Exam Vieirfication System'
description = 'Backend API for managing resources on the Biometric Attendance and Exam Vieirfication System'
api = Api(doc='/fbdocs', version='1.0', title=title, description=description, authorizations=authorizations)


def create_app(config_name):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config_by_env[config_name])
    db.init_app(app)
    mail.init_app(app)
    api.init_app(app)

    # Default error handler
    @app.errorhandler(Exception)
    def handle_exception(error):
        stream_logger.exception(error)
        if not app.debug:
            logger.exception(error)
        response = {
            'message': error.message,
            'success': False
        }
        return response, error.status

    from api.controller import student_api as student_ns
    from api.controller import student_auth_api as student_auth_ns
    from api.controller import course_api as course_ns
    from api.controller import lecturer_api as lecturer_ns
    from api.controller import lecturer_auth_api as lecturer_auth_ns
    from api.controller import hod_api as hod_ns
    from api.controller import hod_auth_api as hod_auth_ns
    from api.controller import dept_api as dept_ns
    from api.controller import auth_verification_api as auth_verification_ns
    from api.controller import current_api as current_ns
    from api.controller import school_api as school_ns
    from api.controller import admin_api as admin_ns
    from api.controller import  admin_auth_api as admin_auth_ns
    api.add_namespace(student_ns, path='/students')
    api.add_namespace(student_auth_ns, path='/students')
    api.add_namespace(course_ns, path='/courses')
    api.add_namespace(lecturer_ns, path='/lecturers')
    api.add_namespace(lecturer_auth_ns, path='/lecturers')
    api.add_namespace(hod_ns, path='/hods')
    api.add_namespace(hod_auth_ns, path='/hods')
    api.add_namespace(dept_ns, path='/departments')
    api.add_namespace(auth_verification_ns, path='/auth')
    api.add_namespace(current_ns, path='/current')
    api.add_namespace(school_ns, path='/schools')
    api.add_namespace(admin_ns, path='/admins')
    api.add_namespace(admin_auth_ns, path='/admins')

    return app

def select_table_name(table):
    return os.environ.get(table)

class AppException(Exception):
    def __init__(self, message, status):
        Exception.__init__(self)
        self.message = message
        self.status = status
