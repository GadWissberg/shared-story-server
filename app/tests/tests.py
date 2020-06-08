import unittest

from flask import Flask
from flask_testing import TestCase
from sqlalchemy import exists
from werkzeug.security import generate_password_hash

from app import User, db, login_manager
from app.models import Story, Paragraph
from app.routes import auth, main
from app.routes.auth import auth_blue_print, ENCRYPT_METHOD
from app.routes.main import create_response, RESPONSE_KEY_SUCCESS, RESPONSE_KEY_DATA, main_blue_print, KEY_ID

OWNER_ID = 1

STORY_ID_1 = 1
STORY_ID_2 = 2

PARAGRAPH = "paragraph"

TITLE = "title"

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
    test_app.register_blueprint(main_blue_print)
    return test_app


class MyTest(TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        test_app = create_app()
        db.init_app(test_app)
        login_manager.init_app(test_app)
        return test_app

    def test_login(self):
        params = dict()
        params[auth.PARAMETER_LOGIN_EMAIL] = MAIL
        params[auth.PARAMETER_LOGIN_PASSWORD] = PASSWORD
        self._mock_user()
        rv = self.client.post('/login', data=params)
        self.assert200(rv)

    def test_create_response(self):
        response = create_response(True)
        print(response)
        self.assert200(response)
        self.assertTrue(response.get_json()[RESPONSE_KEY_SUCCESS])
        self.assertFalse(RESPONSE_KEY_DATA in response.get_json())

    def test_suggest_new_paragraph(self):
        self._mock_user()
        story = Story(TITLE, OWNER_ID)
        db.session.add(story)
        db.session.commit()
        self._mock_session()

        data_object = {main.REQUEST_KEY_STORY_ID: STORY_ID_1, main.REQUEST_KEY_PARAGRAPH: PARAGRAPH}
        response = self.client.post('/paragraph_suggestion', data=data_object)
        self.assert200(response)
        actual_id = response.json[RESPONSE_KEY_DATA][KEY_ID]
        self.assertTrue(db.session.query(exists().where(Paragraph.id == actual_id)).scalar())

        data_object = {main.REQUEST_KEY_STORY_ID: STORY_ID_2, main.REQUEST_KEY_PARAGRAPH: PARAGRAPH}
        response = self.client.post('/paragraph_suggestion', data=data_object)
        self.assert404(response)

    @staticmethod
    def _mock_user():
        user = User(NAME, MAIL, generate_password_hash(PASSWORD, method=ENCRYPT_METHOD))
        db.session.add(user)
        db.session.commit()

    def test_begin_story(self):
        self._mock_user()
        self._mock_session()

        rv = self.client.post('/story', data={main.REQUEST_KEY_TITLE: TITLE, main.REQUEST_KEY_PARAGRAPH: PARAGRAPH})
        self.assert200(rv)
        self.assertTrue(db.session.query(exists().where(Story.title == TITLE)).scalar())

        rv = self.client.post('/story')
        self.assert400(rv)

    def _mock_session(self):
        params = dict()
        params[auth.PARAMETER_LOGIN_EMAIL] = MAIL
        params[auth.PARAMETER_LOGIN_PASSWORD] = PASSWORD
        self.client.post('/login', data=params, follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
