from flask_login import UserMixin

from . import db

PARAGRAPH_SIZE_LIMIT = 512


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False, unique=True)
    first_paragraph_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title, owner_id):
        self.title = title
        self.owner_id = owner_id


class Paragraph(db.Model):
    __tablename__ = 'paragraphs'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, nullable=False, unique=True)
    owner_id = db.Column(db.Integer, nullable=False, unique=True)
    content = db.Column(db.String(PARAGRAPH_SIZE_LIMIT), nullable=False)

    def __init__(self, story_id, owner_id, content):
        self.story_id = story_id
        self.owner_id = owner_id
        self.content = content
