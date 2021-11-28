"""Module for database connectivity"""

from os import path

from flask_sqlalchemy import SQLAlchemy

from flashapp.config import Config

db = SQLAlchemy()


def create_database(app):
    """Creates DB file if it doesn't exists"""
    if not path.exists('flashapp/' + Config.DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
