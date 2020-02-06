"""API schemas for resubs."""

from pydantic import BaseModel, Field

from .user import User


class Resub(BaseModel):
    """Schema for a resub

    A resub is a user-created community, where fans can create related
    posts.
    """
    name: str
    description: str
    owner: User


class CreateResub(BaseModel):
    """Schema for creating a new resub"""
    name: str
    description: str


class EditResub(BaseModel):
    """Schema for editing a resub"""
    description: str = None
    new_owner_username: str = Field(None, description='Transfers ownership when specified')
