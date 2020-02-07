from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Resub(Base):
    __tablename__ = 'resubs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    owner_name = Column(String, ForeignKey('users.name'))

    owner = relationship('User', back_populates='resubs')
    posts = relationship('Post', back_populates='resubs')
    comments = relationship('Comment', back_populates='resubs')