from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base


user_habbit = Table('user_habbit', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('habbit_id', Integer, ForeignKey('habbit.id'))
)
