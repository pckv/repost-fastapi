from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    bio = Column(String)
    # email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    resubs = relationship('Resub', back_populates='users')
    posts = relationship('Post', back_populates='users')
    comments = relationship('Comment', back_populates='users')