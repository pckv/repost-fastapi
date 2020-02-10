"""API schemas for posts."""

from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel

from repost.api.schemas import bind_orm_fields


class Post(BaseModel):
    """Schema for a post in a resub"""
    id: int
    parent_resub_name: str = Field(..., description='Name of the parent resub')
    title: str
    url: Optional[str]
    content: Optional[str]
    author_username: str = Field(..., description='Username of the author of the post')
    created: datetime
    edited: Optional[datetime]

    class Config:
        orm_mode = True
        getter_dict = bind_orm_fields(author_username='author.username', parent_resub_name='parent_resub.name')


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
