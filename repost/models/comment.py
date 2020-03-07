from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from . import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    edited = Column(DateTime(timezone=True), onupdate=func.now())

    author_id = Column(Integer, ForeignKey('users.id'))
    parent_resub_id = Column(Integer, ForeignKey('resubs.id'))
    parent_post_id = Column(Integer, ForeignKey('posts.id'))
    parent_comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)

    author = relationship('User', back_populates='comments')
    parent_resub = relationship('Resub', back_populates='comments')
    parent_post = relationship('Post', back_populates='comments')
    replies = relationship('Comment')
    votes = relationship('CommentVote')


class CommentVote(Base):
    __tablename__ = 'comments_votes'

    comment_id = Column(Integer, ForeignKey('comments.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    vote = Column(Integer)
