"""The Config base class contains settings that are common to all configurations;
 the different subclasses define settings that are specific to a configuration.
  Additional configurations can be added as needed
"""
import os


class Config:
    SECRET_KEY = os.urandom(24)
    CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB')

class TestingConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB')


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG = False



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

}