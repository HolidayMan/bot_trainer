import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .base import Base
from sqlalchemy.orm import relationship


class Plan(Base):

    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(Integer)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref="plans", order_by="User.id")

    TYPE_DAY = 1
    TYPE_WEEK = 2
    TYPE_MONTH = 3
    TYPE_YEAR = 4

    STATUS_OVERDUE = 1
    STATUS_WAIT = 2
    STATUS_DONE = 3
    STATUS_CANCELED = 4

