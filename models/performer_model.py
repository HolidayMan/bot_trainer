from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from .base import Base

from .task_performer_table import task_performer


class Performer(Base):

    __tablename__ = "performer"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)
    phone_number = Column(String(256), nullable=True, unique=False)
    comments = Column(String(256), nullable=True, unique=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=False)
    user = relationship("User", backref=backref("performers", cascade="all,delete"), order_by="User.id")
    tasks = relationship("Task",
                    secondary=task_performer)
    


    def __repr__(self):
        return "<Performer %s>" % self.name
