from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
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
    votes = Column(Integer)

    author_name = Column(String, ForeignKey('users.username'))
    parent_resub_name = Column(String, ForeignKey('resubs.name'))

    author = relationship('User', back_populates='posts')
    parent_resub = relationship('Resub', back_populates='posts')
    comments = relationship('Comment', back_populates='parent_post')
