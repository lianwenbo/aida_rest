
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID') or 'not authorize'
    ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET') or 'secret not auth'
    TOKEN_EXPIRED = 1800
    VERIFY_EXPIRED = 300
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SECRET_KEY = os.urandom(24)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret key not defined by env')
    TOKEN_EXPIRED = 10
    VERIFY_EXPIRED = 3


class ProductionConfig(Config):
    PRODUCT_MODE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
