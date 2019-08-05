import unittest
import os

from flask import Flask
from flask_testing import TestCase
from config import config_by_env, basedir

from api import db

app = Flask(__name__)


class TestConfigTestCase(TestCase):
    def create_app(self):
        app.config.from_object(config_by_env['test'])
        return app

    def test_test_config(self):
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], f'sqlite3://{os.path.join(basedir, "test.db")}')
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(app.config['FLASK_DEBUG'])


class DevelopmentConfigTestCase(TestCase):
    def create_app(self):
        app.config.from_object(config_by_env['dev'])
        app.config['DB_USER'] = os.environ.get('DB_USER')
        app.config['DB_PASS'] = os.environ.get('DB_PASS')
        app.config['DB_NAME'] = os.environ.get('DB_NAME')
        return app

    def test_development_config(self):
        db_user = app.config['DB_USER']
        db_pass = app.config['DB_PASS']
        db_name = app.config['DB_NAME']
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], f'mysql+pymysql://{db_user}:{db_pass}@localhost:3306/{db_name}')
        self.assertTrue(app.config['FLASK_DEBUG'])


class ProductiontConfigTestCase(TestCase):
    def create_app(self):
        app.config.from_object(config_by_env['prod'])
        return app

    def test_production_config(self):
        self.assertFalse(app.config['FLASK_DEBUG'])

if __name__ == "__main__":
    unittest.main()
