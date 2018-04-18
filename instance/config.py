import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'very secret'
    SECRET_KEY = 'this-really-needs-to-be-changed'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # database configurations
    SQLALCHEMY_DATABASE_URI = 'postgresql://prince:prince@localhost/hello_books'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://prince:prince@localhost/hello_books'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


configuration = {
    'staging': StagingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config
}