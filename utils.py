import json

from flask import Response

RESPONSE_KEY_VOTES = "votes"

RESPONSE_KEY_NAME = "name"

RESPONSE_KEY_OWNER = "owner"

RESPONSE_KEY_OWNER_ID = "owner_id"

RESPONSE_KEY_OWNER_NAME = "owner_name"

RESPONSE_KEY_FIRST_PARAGRAPH = "first_paragraph"

RESPONSE_KEY_PARAGRAPHS = "paragraphs"

RESPONSE_KEY_DEADLINE = "deadline"

RESPONSE_KEY_PARTICIPANTS = "participants"

RESPONSE_KEY_SUGGESTIONS = "suggestions"

RESPONSE_KEY_TITLE = "title"

RESPONSE_KEY_MESSAGE = "message"

RESPONSE_KEY_STORIES = "stories"

RESPONSE_KEY_DATA = 'data'

RESPONSE_KEY_SUCCESS = 'success'


def create_response(success, data=None, message=None):
    resp = {
        RESPONSE_KEY_SUCCESS: success
    }
    if data is not None:
        resp[RESPONSE_KEY_DATA] = data
    if message is not None:
        resp[RESPONSE_KEY_MESSAGE] = message
    return Response(json.dumps(resp), mimetype='application/json')
