from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .base import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    first_name = Column(String(64), unique=True)
    username = Column(String(64), unique=True)
    
    def __repr__(self):
        return "<User %s>" % self.username
