from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """ """
    username: str
    bio: str
    avatar_url: Optional[str]


class CreateUser(BaseModel):
    """ """
    username: str
    password: str


class EditUser(BaseModel):
    """ """
    bio: str = None
    avatar_url: str = None
