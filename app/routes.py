from flask import render_template
from flask import request

from app import app

KEY_EMAIL = 'email'
KEY_PASSWORD = 'password'


@app.route('/get_stories')
def get_stories():
    return render_template('stories_list.json')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get(KEY_EMAIL)
    password = request.args.get(KEY_PASSWORD)
    return email
