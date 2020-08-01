import json

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
with open('secrets.json', 'r') as file:
    secrets = json.load(file)
app.config['SQLALCHEMY_DATABASE_URI'] = secrets['sqlalchemy_database_uri']
app.config['SECRET_KEY'] = secrets['secret']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
login_manager = LoginManager(app)
db.init_app(app)
login_manager.init_app(app)

from app import error_handlers

app.register_blueprint(error_handlers.blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from .models import User

from app.routes.auth import auth_blue_print as auth_blueprint, auth_blue_print

app.register_blueprint(auth_blueprint)

from app.routes.main import main_blue_print as main_blueprint

app.register_blueprint(main_blueprint)
