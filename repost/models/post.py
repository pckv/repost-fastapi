from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Table
from sqlalchemy.orm import relationship

from . import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    edited = Column(DateTime(timezone=True), onupdate=func.now())

    author_id = Column(Integer, ForeignKey('users.id'))
    parent_resub_id = Column(Integer, ForeignKey('resubs.id'))

    author = relationship('User', back_populates='posts')
    parent_resub = relationship('Resub', back_populates='posts')
    comments = relationship('Comment', back_populates='parent_post')
    votes = relationship('PostVote')


class PostVote(Base):
    __tablename__ = 'posts_votes'

    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Integer)

    post_id = Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
