"""API schemas for users."""

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """Schema for a user account"""
    username: str
    bio: str
    avatar_url: Optional[str]


class CreateUser(BaseModel):
    """Schema for creating a new user account"""
    username: str
    password: str


class EditUser(BaseModel):
    """ """
    bio: str = None
    avatar_url: str = None
