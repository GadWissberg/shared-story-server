from flask import render_template

from app import app


@app.route('/get_stories')
def index():
    return render_template('stories_list.json')
