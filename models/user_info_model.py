from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship, backref
from .base import Base


class UserInfo(Base):

    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False)
    surname = Column(String(64), unique=False)
    age = Column(Integer, unique=False)
    planning_time = Column(Time, unique=False)
    question1 = Column(String(64), unique=False)
    question2 = Column(String(64), unique=False)
    question3 = Column(String(64), unique=False)
    question4 = Column(String(64), unique=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref=backref("user_info", cascade="all,delete"), order_by="User.id")


    def __repr__(self):
        return "<UserInfo %s>" % self.name
