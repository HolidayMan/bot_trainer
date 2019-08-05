import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .base import Base
from sqlalchemy.orm import relationship, backref


class Plan(Base):

    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(Integer)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref=backref("plans", cascade="all,delete"), order_by="User.id")

    TYPE_DAY = 1
    TYPE_WEEK = 2
    TYPE_MONTH = 3
    TYPE_YEAR = 4

    STATUS_OVERDUE = 1
    STATUS_WAIT = 2
    STATUS_DONE = 3
    STATUS_CANCELED = 4

    def is_overdue(self):
        time_passed = datetime.datetime.utcnow() - self.date_added
        if self.type == self.TYPE_DAY:
            return time_passed > 0
        elif self.type == self.TYPE_WEEK:
            return time_passed > 7
        elif self.type == self.TYPE_MONTH:
            return time_passed > 30
        elif self.type == self.TYPE_YEAR:
            return time_passed > 365
    

    def __repr__(self):
        return '< Plan "%s" for user %s >' % (self.title, self.user.username)
        