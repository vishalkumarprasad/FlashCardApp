from flask import Flask
from flask_login import LoginManager
from flashapp.controller import views
from flashapp.auth import auth
from flashapp.database import db, DB_NAME, create_database, User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'klfaslkdfj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

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



