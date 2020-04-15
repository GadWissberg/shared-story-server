import json

from flask import Blueprint, render_template, request, Response
from flask_login import login_required, current_user

from app import db
from app.models import Story, Paragraph

RESPONSE_KEY_MESSAGE = "message"

RESPONSE_KEY_STORIES = "stories"

RESPONSE_KEY_DATA = 'data'

RESPONSE_KEY_SUCCESS = 'success'

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Index'


def create_response(success, data=None, message=None):
    resp = {
        RESPONSE_KEY_SUCCESS: success
    }
    if data is not None:
        resp[RESPONSE_KEY_DATA] = data
    if message is not None:
        resp[RESPONSE_KEY_MESSAGE] = message
    return Response(json.dumps(resp), mimetype='application/json')


@main.route('/get_stories', methods=['GET'])
@login_required
def get_stories():
    stories = db.session.query().with_entities(Story.id, Story.title).all()
    stories_dict = {}
    for story in stories:
        stories_dict[story.id] = story.title
    return create_response(True, {RESPONSE_KEY_STORIES: stories_dict})


@main.route('/begin_story', methods=['POST'])
@login_required
def begin_story():
    new_story = add_new_story()
    new_paragraph = add_new_paragraph(new_story)
    new_story.first_paragraph_id = new_paragraph.id
    db.session.commit()
    return render_template('response.json', success=1)


def add_new_paragraph(new_story):
    paragraph = request.form.get('paragraph')
    new_paragraph = Paragraph(new_story.id, current_user.id, paragraph)
    db.session.add(new_paragraph)
    db.session.commit()
    return new_paragraph


def add_new_story():
    title = request.form.get('title')
    new_story = Story(title, current_user.id)
    db.session.add(new_story)
    db.session.commit()
    return new_story
