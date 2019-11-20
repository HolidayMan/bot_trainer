from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from .base import Base


class Project(Base):

    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=False)
    user = relationship("User", backref=backref("projects", cascade="all,delete"), order_by="User.id")


    def __eq__(self, other):
        return all([getattr(self, attr) == getattr(other, attr) for attr, value in list(self.__dict__.items())[1:]])


    def __repr__(self):
        return "<Project %s>" % self.name
