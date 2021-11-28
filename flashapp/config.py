"""Module for configuration"""


class Config:
    """Default configuration class"""
    DEBUG = False
    SQLITE_DB_DIR = None
    DB_NAME = "database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dslkjfds3fr34r43'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
