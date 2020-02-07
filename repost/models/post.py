from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created = Column(DateTime)
    edited = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    owner_name = Column(String, ForeignKey('users.name'))
    parent_resub = Column(Integer, ForeignKey('resubs.id'))

    owner = relationship('User', back_populates='posts')
    resub = relationship('Resub', back_populates='posts')
    comments = relationship('Comment', back_populates='posts')
