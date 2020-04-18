import json

from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from app import db
from app.models import Story, Paragraph

MESSAGE_MANDATORY_FIELD_WAS_NOT_SUPPLIED = "The mandatory field was not supplied: {0}"

MAX_SIZE_TITLE = 64
MAX_SIZE_PARAGRAPH = 256

MESSAGE_CANNOT_BE_EMPTY = "The parameter {0} cannot be empty!"

REQUEST_KEY_TITLE = 'title'

REQUEST_KEY_PARAGRAPH = 'paragraph'

RESPONSE_KEY_ID = "id"

RESPONSE_KEY_MESSAGE = "message"

RESPONSE_KEY_STORIES = "stories"

RESPONSE_KEY_DATA = 'data'

RESPONSE_KEY_SUCCESS = 'success'

main = Blueprint('main', __name__)


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
    validate_request_for_new_story()
    new_story = add_new_story()
    add_new_paragraph(new_story)
    return create_response(True, {RESPONSE_KEY_ID: new_story.id})


def add_new_paragraph(new_story):
    paragraph = request.form.get(REQUEST_KEY_PARAGRAPH)
    new_paragraph = Paragraph(new_story.id, current_user.id, paragraph)
    db.session.add(new_paragraph)
    db.session.commit()
    new_story.first_paragraph_id = new_paragraph.id
    db.session.commit()
    return new_paragraph


def validate_request_for_new_story():
    failure_message = check_parameter_length(REQUEST_KEY_TITLE, MAX_SIZE_TITLE)
    if failure_message is None:
        failure_message = check_parameter_length(REQUEST_KEY_PARAGRAPH, MAX_SIZE_PARAGRAPH)
    if failure_message is not None:
        abort(400, description=failure_message)


def check_parameter_length(parameter, max_size):
    failure_message = None
    if parameter not in request.form:
        failure_message = MESSAGE_MANDATORY_FIELD_WAS_NOT_SUPPLIED.format(parameter)
    elif len(request.form.get(parameter)) == 0:
        failure_message = MESSAGE_CANNOT_BE_EMPTY.format(parameter)
    elif len(request.form.get(parameter)) > max_size:
        failure_message = MESSAGE_CANNOT_BE_EMPTY.format(parameter)
    return failure_message


def add_new_story():
    title = request.form.get(REQUEST_KEY_TITLE)
    new_story = Story(title, current_user.id)
    db.session.add(new_story)
    db.session.commit()
    return new_story
