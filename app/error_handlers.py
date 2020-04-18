import flask

from app.routes.main import create_response, RESPONSE_KEY_MESSAGE

blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(401)
def handle401(e):
    return create_response(False, {RESPONSE_KEY_MESSAGE: e.description}), 401


@blueprint.app_errorhandler(400)
def handle400(e):
    return create_response(False, {RESPONSE_KEY_MESSAGE: e.description}), 400
