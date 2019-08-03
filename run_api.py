import os
import sys
import unittest

from dotenv import load_dotenv
from flask_migrate import Migrate

from api import create_app, db

load_dotenv()

if os.environ.get('FLASK_ENV') is None:
    print('FLASK_ENV not provided')
    sys.exit()

app = create_app(os.environ.get('FLASK_ENV'))
app.app_context().push()

migrate = Migrate(app, db)

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return True
    else:
        return False

from utils import cli_utils
