from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config

DB = 'postgresql://postgres:fatcow@localhost/mututale'

app = Flask(__name__)
app.config.from_object(Config)
engine = create_engine(DB)
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

from app import models
from app import routes
