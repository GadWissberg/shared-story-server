from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fatcow@localhost/mututale'
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from app.routes.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from app.routes.main import main as main_blueprint

app.register_blueprint(main_blueprint)
