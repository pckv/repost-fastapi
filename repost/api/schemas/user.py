from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """ The User schema to be returned as a response from the API. """
    username: str
    bio: str
    avatar_url: Optional[str]


class UserCreate(BaseModel):
    """ The user schema used to create a new User. """
    username: str
    password: str
