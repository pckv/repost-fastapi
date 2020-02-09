"""API schemas for users."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """Schema for a user account"""
    username: str
    bio: str
    avatar_url: Optional[str]
    created: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    """Schema for creating a new user account"""
    username: str
    password: str


class EditUser(BaseModel):
    """Schema for editing a user account"""
    bio: str = None
    avatar_url: str = None
