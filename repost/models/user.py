from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    bio = Column(String)
    avatar_url = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    edited = Column(DateTime(timezone=True), onupdate=func.now())

    hashed_password = Column(String)

    resubs = relationship('Resub', back_populates='owner')
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')
