from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship, backref

class Chat(Base):

    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", backref=backref("chat", cascade="all,delete"), order_by="User.id")

    def __repr__(self):
        return "<Chat with user %s>" % self.user.username