from flask_sqlalchemy import SQLAlchemy

from app.ourtale import webapp

db = SQLAlchemy()
db.init_app(webapp)
