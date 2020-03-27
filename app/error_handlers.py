import flask
from flask import render_template

blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(401)
def handle401(e):
    return render_template("response.json", success=0, message=e.description), 401
