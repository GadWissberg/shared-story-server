import json

from flask import Blueprint, request, Response
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from app import db
from app.models import Story, Paragraph, User

MESSAGE_STORY_WAS_NOT_FOUND = "Story with id {0} was not found"

RESPONSE_KEY_NAME = "name"

RESPONSE_KEY_OWNER = "owner"

RESPONSE_KEY_OWNER_ID = "owner_id"

RESPONSE_KEY_OWNER_NAME = "owner_name"

RESPONSE_KEY_FIRST_PARAGRAPH = "first_paragraph"

RESPONSE_KEY_PARAGRAPHS = "paragraphs"

RESPONSE_KEY_SUGGESTIONS = "suggestions"

RESPONSE_KEY_TITLE = "title"

MESSAGE_MANDATORY_FIELD_WAS_NOT_SUPPLIED = "The mandatory field was not supplied: {0}"

MAX_SIZE_TITLE = 64

MAX_SIZE_PARAGRAPH = 1200

MESSAGE_CANNOT_BE_EMPTY = "The parameter {0} cannot be empty!"

MESSAGE_TOO_LONG = "The given {0} exceeds the max-size: {1}"

REQUEST_KEY_TITLE = 'title'

REQUEST_KEY_PARAGRAPH = 'paragraph'

REQUEST_KEY_STORY_ID = "story_id"

KEY_ID = "id"

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
    _add_new_paragraph_to_story(new_story, request.form.get(REQUEST_KEY_PARAGRAPH))
    return create_response(True, {KEY_ID: new_story.id})


def _add_new_paragraph_to_story(story, paragraph_content=None):
    paragraph_entry = _add_new_paragraph(paragraph_content, story.id)
    story.paragraphs = '[]' if story.paragraphs is None else story.paragraphs
    paragraphs_order = json.loads(story.paragraphs)
    paragraphs_order.append(paragraph_entry.id)
    story.paragraphs = json.dumps(paragraphs_order)
    db.session.commit()
    return paragraph_entry


def _add_new_paragraph(paragraph_content, story_id):
    paragraph_entry = Paragraph(story_id, current_user.id, paragraph_content)
    db.session.add(paragraph_entry)
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
        failure_message = MESSAGE_TOO_LONG.format(parameter, max_size)
    return failure_message


def _add_new_story():
    title = request.form.get(REQUEST_KEY_TITLE)
    story = Story(title, current_user.id)
    db.session.add(story)
    db.session.commit()
    return story


@main_blue_print.route('/paragraph_suggestion', methods=['POST'])
@login_required
def suggest_new_paragraph():
    story_id = request.form.get(REQUEST_KEY_STORY_ID)
    story = Story.query.get(story_id)
    if story is None:
        abort(404, description=MESSAGE_STORY_WAS_NOT_FOUND.format(story_id))
    paragraph = _add_new_suggestion_to_story(story, story_id)
    db.session.commit()
    return create_response(True, {KEY_ID: paragraph.id})


def _add_new_suggestion_to_story(story, story_id):
    paragraph = _add_new_paragraph(request.form.get(REQUEST_KEY_PARAGRAPH), story_id)
    story.suggestions = '[]' if story.suggestions is None else story.suggestions
    suggestions_order = json.loads(story.suggestions)
    suggestions_order.append(paragraph.id)
    story.suggestions = json.dumps(suggestions_order)
    return paragraph


@main_blue_print.route('/paragraph_suggestion', methods=['GET'])
@login_required
def get_paragraphs_suggestions():
    suggestions = []
    if REQUEST_KEY_STORY_ID in request.args:
        suggestions = _get_suggested_paragraphs_by_story(suggestions)
    else:
        abort(400, description=MESSAGE_MANDATORY_FIELD_WAS_NOT_SUPPLIED.format(REQUEST_KEY_STORY_ID))
    return create_response(True, suggestions)


def _get_suggested_paragraphs_by_story(suggestions):
    story = Story.query.get(request.args.get(REQUEST_KEY_STORY_ID))
    suggestions_ids = json.loads(story.suggestions)
    for suggestion_id in suggestions_ids:
        suggestion = Paragraph.query.get(suggestion_id)
        suggestions.append(suggestion.as_dict())
    return suggestions


@main_blue_print.route('/story', methods=['GET'])
@login_required
def get_story():
    if KEY_ID in request.args:
        response_data = _get_story_by_id()
    else:
        response_data = _get_stories()
    return create_response(True, response_data)


def _get_stories():
    stories = db.session.query().with_entities(Story.id, Story.title, Story.owner_id, Story.paragraphs).all()
    owners_dict = _get_owners_as_dict()
    stories_dict = _get_stories_as_dict(owners_dict, stories)
    return {RESPONSE_KEY_STORIES: stories_dict}


def _get_stories_as_dict(owners_dict, stories):
    paragraphs_to_fetch = []
    stories_dict = {}
    for story in stories:
        _add_story_to_stories_dict(owners_dict, paragraphs_to_fetch, stories_dict, story)
    paragraphs = db.session.query(Paragraph).filter(Paragraph.id.in_(paragraphs_to_fetch)).all()
    for paragraph in paragraphs:
        stories_dict[paragraph.story_id][RESPONSE_KEY_FIRST_PARAGRAPH] = paragraph.as_dict()
    return stories_dict


def _add_story_to_stories_dict(owners_dict, paragraphs_to_fetch, stories_dict, story):
    owner = dict(zip(owners_dict[story.owner_id].keys(), owners_dict[story.owner_id]))
    stories_dict[story.id] = {RESPONSE_KEY_TITLE: story.title, RESPONSE_KEY_OWNER: owner}
    story_paragraphs = story.paragraphs
    if story_paragraphs is not None:
        paragraphs = json.loads(story_paragraphs)
        paragraphs_to_fetch.append(paragraphs[0])


def _get_owners_as_dict():
    owners = db.session.query().with_entities(User.id, User.name).all()
    owners_dict = {}
    for owner in owners:
        owners_dict[owner.id] = owner
    return owners_dict


def _get_story_by_id():
    story = Story.query.get(request.args.get(KEY_ID))
    owner = User.query.get(story.owner_id)
    paragraphs_order = json.loads(story.paragraphs)
    paragraphs = []
    for paragraph_id in paragraphs_order:
        paragraph = Paragraph.query.get(paragraph_id)
        paragraphs.append(paragraph.as_dict())
    suggestions = []
    if story.suggestions is not None:
        suggestions_order = json.loads(story.suggestions)
        for suggestion_id in suggestions_order:
            paragraph = Paragraph.query.get(suggestion_id)
            suggestions.append(paragraph.as_dict())
    response_data = {RESPONSE_KEY_TITLE: story.title,
                     RESPONSE_KEY_OWNER: {KEY_ID: story.owner_id, RESPONSE_KEY_NAME: owner.name},
                     RESPONSE_KEY_PARAGRAPHS: paragraphs,
                     RESPONSE_KEY_SUGGESTIONS: suggestions}
    return response_data
