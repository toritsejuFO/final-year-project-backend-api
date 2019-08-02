import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite3://{os.path.join(basedir, "test.db")}'


class ProductinConfig(Config):
    FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

config_by_env = {
    'dev': DevelopmentConfig,
    'test': TestConfig,
    'prod':ProductinConfig
}

jwt_key = Config.JWT_SECRET_KEY

if __name__ == '__main__':
    print(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
