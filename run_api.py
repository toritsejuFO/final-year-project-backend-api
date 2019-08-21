import os
import sys
import unittest

import arrow
from flask import request
from dotenv import load_dotenv
from flask_migrate import Migrate

from api import create_app, db
from logger import request_logger
from api.model import Student, Level, School, Department, Course, Semester, HOD, RevokedToken

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
        'db': db,
        'Student': Student,
        'Level': Level,
        'School': School, 
        'Department': Department, 
        'Course': Course,
        'Semester': Semester,
        'HOD': HOD,
        'RevokedToken': RevokedToken
    }

@app.cli.command()
def run():
    app.run(host='0.0.0.0')

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return True
    else:
        return False

@app.after_request
def log_info(response):
    date = arrow.now('Africa/Lagos')
    log_details = {
        'date': str(date),
        'user_ip': request.remote_addr,
        'browser': request.user_agent.browser,
        'user_device': request.user_agent.platform,
        'method': request.method,
        'request_url': request.url,
        'status_code': response.status_code,
    }
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, x-auth-token')
    request_logger.warning(log_details)
    app.logger.info(log_details)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')

from utils import cli_utils
