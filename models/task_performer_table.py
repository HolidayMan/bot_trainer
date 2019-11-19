from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base


task_performer = Table('task_performer', Base.metadata,
    Column('performer_id', Integer, ForeignKey('performer.id')),
    Column('task_id', Integer, ForeignKey('task.id'))
)
