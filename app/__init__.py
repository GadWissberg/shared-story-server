from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app import error_handlers

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fatcow@localhost/mututale'
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(error_handlers.blueprint)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from .models import User

from app.routes.auth import auth_blue_print as auth_blueprint, auth_blue_print

app.register_blueprint(auth_blueprint)

from app.routes.main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    db.init_app(app)
    app.register_blueprint(auth_blue_print)
    login_manager.init_app(app)
