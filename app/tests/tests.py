import unittest

from flask import Flask
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from app import User, db, login_manager
from app.routes import auth
from app.routes.auth import auth_blue_print, ENCRYPT_METHOD
from app.routes.main import create_response, RESPONSE_KEY_SUCCESS, RESPONSE_KEY_DATA

NAME = "gad"

MAIL = "gadw17@gmail.com"
PASSWORD = "Aa123456"


def create_app():
    test_app = Flask(__name__, template_folder='../templates')
    test_app.config['TESTING'] = True
    test_app.config['LIVESERVER_TIMEOUT'] = 10
    test_app.config['SESSION_TYPE'] = 'filesystem'
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    test_app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO1'
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    test_app.register_blueprint(auth_blue_print)
    return test_app


class MyTest(TestCase):

    def create_app(self):
        test_app = create_app()
        db.init_app(test_app)
        test_app.register_blueprint(auth_blue_print)
        login_manager.init_app(test_app)
        return test_app

    def test_login(self):
        params = dict()
        params[auth.PARAMETER_LOGIN_EMAIL] = MAIL
        params[auth.PARAMETER_LOGIN_PASSWORD] = PASSWORD
        user = User(NAME, MAIL, generate_password_hash(PASSWORD, method=ENCRYPT_METHOD))
        db.session.add(user)
        db.session.commit()
        rv = self.client.post('/login', data=params)
        self.assert200(rv)

    def test_create_response(self):
        response = create_response(True)
        print(response)
        self.assert200(response)
        self.assertTrue(response.get_json()[RESPONSE_KEY_SUCCESS])
        self.assertFalse(RESPONSE_KEY_DATA in response.get_json())

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
