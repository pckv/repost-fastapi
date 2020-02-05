"""API schemas for resubs."""

from pydantic import BaseModel, Field

from .user import User


class Resub(BaseModel):
    """ The Resub schema to be returned as a response from the API. """
    name: str
    description: str
    owner: User


class CreateResub(BaseModel):
    name: str
    description: str


class EditResub(BaseModel):
    description: str = None
    new_owner_username: str = Field(None, description='Transfers ownership when specified')
