"""API schemas for comments."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .user import User


class Comment(BaseModel):
    """Schema for a comment in a post"""
    id: int
    parent_id: int = Field(..., description='ID of the comment\'s parent post or comment')
    content: str
    author: User
    created: datetime
    edited: Optional[datetime]
    votes: int


class CreateComment(BaseModel):
    content: str


class EditComment(BaseModel):
    content: str = None


class Vote(str, Enum):
    upvote = 'upvote'
    downvote = 'downvote'
    novote = 'novote'
