"""App Module to create the web-app"""

from flask import Flask
from flask_login import LoginManager

from flashapp.auth import auth
from flashapp.config import Config
from flashapp.controller import views
from flashapp.database import db, create_database, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



