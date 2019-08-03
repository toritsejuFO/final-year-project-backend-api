import os
import sys

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

@app.cli.command('tod')
def test():
    print('Testing 1 2...')

from utils import cli_utils
