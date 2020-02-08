from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created = Column(DateTime)
    edited = Column(DateTime, nullable=True)

    author_name = Column(String, ForeignKey('users.id'))
    parent_resub_name = Column(String, ForeignKey('resubs.name'))
    parent_post_name = Column(String, ForeignKey('posts.title'))
    parent_comment_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
    votes = Column(Integer)

    author = relationship('User', back_populates='comments')
    parent_resub = relationship('Resub', back_populates='comments')
    parent_post = relationship('Post', back_populates='comments')

    replies = relationship('Comment')
