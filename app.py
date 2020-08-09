import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ['SECRET']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
login_manager = LoginManager(app)
db.init_app(app)
login_manager.init_app(app)

from . import error_handlers

app.register_blueprint(error_handlers.blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from .models import User

from app.routes.auth import auth_blue_print as auth_blueprint

app.register_blueprint(auth_blueprint)

from app.routes.main import main_blue_print as main_blueprint

app.register_blueprint(main_blueprint)
