from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    done = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    owner = relationship("User", back_populates="tasks")
