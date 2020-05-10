import json

from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from app import db
from app.models import Story, Paragraph, User

RESPONSE_KEY_NAME = "name"

RESPONSE_KEY_OWNER = "owner"
RESPONSE_KEY_OWNER_ID = "owner_id"

RESPONSE_KEY_PARAGRAPHS = "paragraphs"

RESPONSE_KEY_TITLE = "title"

MESSAGE_MANDATORY_FIELD_WAS_NOT_SUPPLIED = "The mandatory field was not supplied: {0}"

MAX_SIZE_TITLE = 64
MAX_SIZE_PARAGRAPH = 256

MESSAGE_CANNOT_BE_EMPTY = "The parameter {0} cannot be empty!"

REQUEST_KEY_TITLE = 'title'

REQUEST_KEY_PARAGRAPH = 'paragraph'

REQUEST_KEY_ID = "id"

RESPONSE_KEY_ID = "id"

RESPONSE_KEY_MESSAGE = "message"

RESPONSE_KEY_STORIES = "stories"

RESPONSE_KEY_DATA = 'data'

RESPONSE_KEY_SUCCESS = 'success'

main_blue_print = Blueprint('main', __name__)


##
# @param success Whether response is success.
# @param data Additional optional dictionary.
# @param message Additional message.
# @return A flask wrapper response
def create_response(success, data=None, message=None):
    resp = {
        RESPONSE_KEY_SUCCESS: success
    }
    if data is not None:
        resp[RESPONSE_KEY_DATA] = data
    if message is not None:
        resp[RESPONSE_KEY_MESSAGE] = message
    return Response(json.dumps(resp), mimetype='application/json')


@main_blue_print.route('/story', methods=['POST'])
@login_required
def begin_story():
    _validate_request_for_new_story()
    new_story = _add_new_story()
    _add_new_paragraph(new_story)
    return create_response(True, {RESPONSE_KEY_ID: new_story.id})


def _add_new_paragraph(story):
    paragraph_entry = Paragraph(story.id, current_user.id, request.form.get(REQUEST_KEY_PARAGRAPH))
    db.session.add(paragraph_entry)
    db.session.commit()
    story.paragraphs = [] if story.paragraphs is None else story.paragraphs
    story.paragraphs.append(paragraph_entry.id)
    story.paragraphs = json.dumps(story.paragraphs)
    db.session.commit()
    return paragraph_entry


def _validate_request_for_new_story():
    failure_message = _check_parameter_length(REQUEST_KEY_TITLE, MAX_SIZE_TITLE)
    if failure_message is None:
        failure_message = _check_parameter_length(REQUEST_KEY_PARAGRAPH, MAX_SIZE_PARAGRAPH)
    if failure_message is not None:
        abort(400, description=failure_message)


def _check_parameter_length(parameter, max_size):
    failure_message = None
    if parameter not in request.form:
        failure_message = MESSAGE_MANDATORY_FIELD_WAS_NOT_SUPPLIED.format(parameter)
    elif len(request.form.get(parameter)) == 0:
        failure_message = MESSAGE_CANNOT_BE_EMPTY.format(parameter)
    elif len(request.form.get(parameter)) > max_size:
        failure_message = MESSAGE_CANNOT_BE_EMPTY.format(parameter)
    return failure_message


def _add_new_story():
    title = request.form.get(REQUEST_KEY_TITLE)
    story = Story(title, current_user.id)
    db.session.add(story)
    db.session.commit()
    return story


@main_blue_print.route('/story', methods=['GET'])
@login_required
def get_story():
    if REQUEST_KEY_ID in request.args:
        response_data = _get_story_by_id()
    else:
        response_data = _get_stories()
    return create_response(True, response_data)


def _get_stories():
    stories = db.session.query().with_entities(Story.id, Story.title, Story.owner_id).all()
    stories_dict = {}
    for story in stories:
        stories_dict[story.id] = {RESPONSE_KEY_TITLE: story.title, RESPONSE_KEY_OWNER: story.owner_id}
    response_data = {RESPONSE_KEY_STORIES: stories_dict}
    return response_data


def _get_story_by_id():
    story = Story.query.get(request.args.get(REQUEST_KEY_ID))
    owner = User.query.get(story.owner_id)
    paragraphs_order = json.loads(story.paragraphs)
    paragraphs = []
    for paragraph_id in paragraphs_order:
        paragraph = Paragraph.query.get(paragraph_id)
        paragraphs.append(paragraph.as_dict())
    response_data = {RESPONSE_KEY_TITLE: story.title,
                     RESPONSE_KEY_OWNER: {RESPONSE_KEY_ID: story.owner_id, RESPONSE_KEY_NAME: owner.name},
                     RESPONSE_KEY_PARAGRAPHS: paragraphs}
    return response_data
