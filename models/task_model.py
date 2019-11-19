from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from .base import Base

from .task_performer_table import task_performer


class Task(Base):

    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False)
    date_start = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    comments = Column(String(256), nullable=True)
    completed = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False, unique=False)
    project = relationship("Project", backref=backref("tasks", cascade="all,delete"), order_by="Project.id")
    # dependencies_id = Column(Integer, ForeignKey('task.id'), nullable=True, unique=False)
    # dependencies = relationship("Task", backref=backref("tasks", cascade="all,delete"), order_by="Task.id")
    performers = relationship("Performer",
                    secondary=task_performer)
    

    def __repr__(self):
        return "<Task %s>" % self.name
