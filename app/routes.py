from flask import render_template

from app import app
from app import connection


@app.route('/get_stories')
def index():
    return render_template('stories_list.json')


@app.route('/test')
def test():
    fetch_query = connection.execute("SELECT * FROM users")
    for data in fetch_query.fetchall():
        return str(data)
