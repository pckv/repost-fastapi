"""API schemas for comments."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Schema for a comment in a post"""
    id: int
    parent_resub_name: str = Field(..., description='Name of the parent resub the comment was created in')
    parent_post_id: int = Field(..., description='ID of the parent post the comment was created in')
    parent_comment_id: Optional[int] = Field(..., description='ID of the parent comment when the comment is a reply')
    content: str
    author_name: str
    created: datetime
    edited: Optional[datetime]
    votes: int


class CreateComment(BaseModel):
    """Schema for creating a comment in a post"""
    content: str


class EditComment(BaseModel):
    """Schema for editing a comment in a post"""
    content: str = None
