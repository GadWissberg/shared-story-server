from flask import Flask
from sqlalchemy import create_engine

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
engine = create_engine('postgresql://postgres:fatcow@localhost/mututale')
connection = engine.connect()
print("DB Instance created")

from app import routes
