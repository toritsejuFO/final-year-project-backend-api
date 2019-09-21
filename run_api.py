import os
import sys
import unittest

import arrow
from flask import request
from dotenv import load_dotenv
from flask_migrate import Migrate

from api import create_app, db
from api.model import Student, Level, School, Department, Course, Semester, HOD, RevokedToken, Lecturer
from logger import request_logger, stream_logger

load_dotenv()

if os.environ.get('FLASK_ENV') is None:
    print('FLASK_ENV not provided')
    sys.exit()

app = create_app(os.environ.get('FLASK_ENV'))
app.app_context().push()

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'Student': Student,
        'Level': Level,
        'School': School, 
        'Department': Department, 
        'Course': Course,
        'Semester': Semester,
        'HOD': HOD,
        'RevokedToken': RevokedToken, 
        'Lecturer': Lecturer
    }

@app.cli.command()
def run():
    app.run(host='0.0.0.0')

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()

@app.after_request
def log_info(response):
    date = arrow.now('Africa/Lagos')
    if os.environ.get('FLASK_ENV') is 'prod':
        ip = request.headers.get(app.config['REAL_IP'])
    else:
        ip = request.remote_addr
    log_details = {
        'date': date.format(),
        'ip': ip,
        'browser': request.user_agent.browser,
        'device': request.user_agent.platform,
        'status_code': response.status_code,
        'path': request.path,
        'method': request.method,
    }
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, x-auth-token')
    stream_logger.debug(log_details)
    if not app.debug:
        request_logger.info(log_details)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')

from utils import cli_utils
