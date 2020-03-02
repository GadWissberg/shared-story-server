from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from app import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(50), nullable=False)


Base.metadata.create_all(engine)
