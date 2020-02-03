from typing import Optional, List

from pydantic import BaseModel

from repost.api.schemas import Resub, Post, Comment


class User(BaseModel):
    """ The User schema to be returned as a response from the API. """
    username: str
    bio: str
    avatar_url: Optional[str]
    resubs: List[Resub]
    posts: List[Post]
    comments: List[Comment]


class UserCreate(BaseModel):
    """ The user schema used to create a new User. """
    username: str
    password: str
