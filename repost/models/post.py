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

    author_id = Column(String, ForeignKey('users.id'))
    parent_resub_id = Column(String, ForeignKey('resubs.id'))

    author = relationship('User', back_populates='posts')
    parent_resub = relationship('Resub', back_populates='posts')
    comments = relationship('Comment', back_populates='parent_post')
