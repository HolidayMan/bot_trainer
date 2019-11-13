from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from .base import Base
from .user_habbit_table import user_habbit


class Studying(Base):

    __tablename__ = "studying"

    id = Column(Integer, primary_key=True)
    state = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    user = relationship("User", backref=backref("studying", cascade="all,delete"), order_by="User.id")


    STATE_USING = 0
    STATE_ONE_TASK = 1
    STATE_CHECK_LIST = 2
    STATE_GANT_DIAGRAM = 3


    def __repr__(self):
        return "<Studying %s>" % self.user.username