import os
from sqlite3 import PARSE_COLNAMES, PARSE_DECLTYPES


class Config(object):
    DEBUG = False
    TESTING = False


class LocalConfig(Config):
    ENVIRONMENT = "local"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")


class TestConfig(Config):
    TESTING = True
    ENVIRONMENT = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"detect_types": PARSE_DECLTYPES | PARSE_COLNAMES}}
