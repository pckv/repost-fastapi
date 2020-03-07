"""API schemas for comments."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from repost.api.schemas import bind_orm_fields


class Comment(BaseModel):
    """Schema for a comment in a post"""
    id: int
    parent_resub_name: str = Field(..., description='Name of the parent resub the comment was created in')
    parent_post_id: int = Field(..., description='ID of the parent post the comment was created in')
    parent_comment_id: Optional[int] = Field(..., description='ID of the parent comment when the comment is a reply')
    content: str
    author_username: str = Field(..., description='Username of the author of the comment')
    created: datetime
    edited: Optional[datetime]
    votes: int = 0

    class Config:
        orm_mode = True
        getter_dict = bind_orm_fields(author_username='author.username', parent_resub_name='parent_resub.name',
                                      votes=lambda comment: sum(v.vote for v in comment.votes))


class CreateComment(BaseModel):
    """Schema for creating a comment in a post"""
    content: str


class EditComment(BaseModel):
    """Schema for editing a comment in a post"""
    content: str
