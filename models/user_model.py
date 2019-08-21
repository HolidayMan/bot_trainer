from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user_habbit_table import user_habbit


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    first_name = Column(String(64), unique=False)
    username = Column(String(64), unique=True)
    habbits = relationship("Habbit",
                    secondary=user_habbit)


    def __repr__(self):
        return "<User %s>" % self.username
