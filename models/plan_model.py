from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from .base import Base
import datetime
import calendar


def get_ua_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)


class Plan(Base):

    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    date_added = Column(DateTime, default=get_ua_time)
    type = Column(Integer)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref=backref("plans", cascade="all,delete"), order_by="User.id")

    TYPE_TODAY = 0
    TYPE_DAY = 1
    TYPE_WEEK = 2
    TYPE_MONTH = 3
    TYPE_YEAR = 4

    STATUS_OVERDUE = 1
    STATUS_WAIT = 2
    STATUS_DONE = 3
    STATUS_CANCELED = 4

    def is_overdue(self):
        delta = datetime.timedelta(days=1) - datetime.timedelta(
                            hours=self.date_added.time().hour, 
                            minutes=self.date_added.time().minute, 
                            seconds=self.date_added.time().second
                        )
        if self.type == self.TYPE_TODAY:
            tomorrow = self.date_added + delta
            return get_ua_time() > tomorrow
        elif self.type == self.TYPE_DAY:
            after_tomorrow= self.date_added + datetime.timedelta(days=1) + delta
            return get_ua_time() > after_tomorrow
        elif self.type == self.TYPE_WEEK:
            after_week = self.date_added + datetime.timedelta(days=7) + delta
            return get_ua_time() > after_week
        elif self.type == self.TYPE_MONTH:
            curr_month_days = calendar.monthrange(self.date_added.year, self.date_added.month)[1]
            after_month = self.date_added + datetime.timedelta(days=curr_month_days) + delta
            return get_ua_time() > after_month
        elif self.type == self.TYPE_YEAR:
            after_year = self.date_added + datetime.timedelta(days=365) + delta
            return get_ua_time() > after_year
    

    def __repr__(self):
        return '< Plan "%s" for user %s >' % (self.title, self.user.username)
        