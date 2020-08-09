import flask

from app.ourtale.routes.main import create_response

blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(401)
def handle401(e):
    return create_response(False, message=e.description), 401


@blueprint.app_errorhandler(400)
def handle400(e):
    return create_response(False, message=e.description), 400


@blueprint.app_errorhandler(404)
def handle404(e):
    return create_response(False, message=e.description), 404


@blueprint.app_errorhandler(409)
def handle409(e):
    return create_response(False, message=e.description), 409
