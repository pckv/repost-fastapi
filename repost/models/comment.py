from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=True)
    created = Column(DateTime)
    edited = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    owner_name = Column(String, ForeignKey('users.name'))
    parent_resub = Column(Integer, ForeignKey('resubs.id'))
    parent_post = Column(Integer, ForeignKey('posts.id'))

    owner = relationship('User', back_populates='comments')
    resub = relationship('Resub', back_populates='comments')
    post = relationship('Post', back_populates='comments')