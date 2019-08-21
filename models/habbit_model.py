from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .user_habbit_table import user_habbit
from .base import Base


class Habbit(Base):
    __tablename__ = "habbit"

    id = Column(Integer, primary_key=True)
    en_name = Column(String, unique=True)
    ru_name = Column(String, unique=True)
    users = relationship("User",
                    secondary=user_habbit)

    def __repr__(self):
        return "<Habbit %s>" % self.en_name

