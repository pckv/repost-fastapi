from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Resub(Base):
    __tablename__ = 'resubs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='resubs')
    posts = relationship('Post', back_populates='parent_resub')
    comments = relationship('Comment', back_populates='parent_resub')
