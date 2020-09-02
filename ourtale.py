import os

from flask import Flask
from flask_login import LoginManager

webapp = Flask(__name__)

webapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
webapp.config['SECRET_KEY'] = os.environ['SECRET']
webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    webapp.run(debug=True, host='0.0.0.0')

from app.models import User

login_manager = LoginManager(webapp)

login_manager.init_app(webapp)

from app import error_handlers

webapp.register_blueprint(error_handlers.blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from app.routes.auth import auth_blue_print as auth_blueprint

webapp.register_blueprint(auth_blueprint)

from app.routes.main import main_blue_print as main_blueprint

webapp.register_blueprint(main_blueprint)
