from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app import db
from app.models import Story, Paragraph

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Index'


@main.route('/get_stories', methods=['GET'])
@login_required
def get_stories():
    return render_template('stories_list.json')


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
