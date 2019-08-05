from flask_testing import TestCase

from api import db
from run_api import app
from config import config_by_env

from utils.populate_departments_table import populate_departments_table
from utils.populate_levels_table import populate_levels_table
from utils.populate_schools_table import populate_schools_table


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object(config_by_env['test'])
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        populate_levels_table()
        populate_schools_table()
        populate_departments_table()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
