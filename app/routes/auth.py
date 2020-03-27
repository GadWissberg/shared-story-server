from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

MESSAGE_WELCOME = "Welcome {}!"

PARAMETER_LOGIN_PASSWORD = 'password'
PARAMETER_LOGIN_EMAIL = 'email'
MESSAGE_WRONG_CREDENTIALS = 'Given credentials are wrong.'

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get(PARAMETER_LOGIN_EMAIL)
    password = request.form.get(PARAMETER_LOGIN_PASSWORD)
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return abort(401, description=MESSAGE_WRONG_CREDENTIALS)
    login_user(user, remember=remember)
    return render_template("response.json", success=1, message=(MESSAGE_WELCOME.format(user.name)))


@auth.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logout'