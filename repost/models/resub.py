from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Resub(Base):
    __tablename__ = 'resubs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    edited = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='resubs')
    posts = relationship('Post', back_populates='parent_resub')
    comments = relationship('Comment', back_populates='parent_resub')
