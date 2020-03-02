from flask import render_template
from flask import request

from app import app, session
from app.models import User

QUERY_CHECK_LOGIN = "select * from users where name=\'{0}\' and password=\'{1}\'"

KEY_EMAIL = 'email'
KEY_PASSWORD = 'password'


@app.route('/get_stories')
def get_stories():
    return render_template('stories_list.json')


@app.route('/login', methods=['POST'])
def login():
    request_email = request.form.get(KEY_EMAIL)
    request_password = request.form.get(KEY_PASSWORD)
    result = session.query(User).filter_by(email=request_email, password=request_password)
    if result.count() != 0:
        logged_user = result.first()
        session.add(logged_user)
    return str(result.count() != 0)
