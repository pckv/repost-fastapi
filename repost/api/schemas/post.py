"""API schemas for posts."""


from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel

from .user import User


class Post(BaseModel):
    """Schema for a post in a resub"""
    id: int
    parent_name: int = Field(..., description='Name of the parent post')
    title: str
    url: Optional[str]
    content: Optional[str]
    author: User
    created: datetime
    edited: Optional[datetime]
    votes: int


class CreatePost(BaseModel):
    """Schema for creating a new post in a resub"""
    title: str
    url: Optional[str]
    content: Optional[str]


class EditPost(BaseModel):
    """Schema for editing a post in a resub"""
    title: str = None
    url: Optional[str] = None
    content: Optional[str] = None
