from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Index'


@main.route('/get_stories')
@login_required
def get_stories():
    return render_template('stories_list.json')
