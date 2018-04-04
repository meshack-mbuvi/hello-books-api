import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'very secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = 'access'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


configuration = {
    'staging': StagingConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config
}