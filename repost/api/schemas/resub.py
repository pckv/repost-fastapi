from typing import List

from pydantic import BaseModel

from repost.api.schemas import User, Post


class Resub(BaseModel):
    """ The Resub schema to be returned as a response from the API. """
    name: str
    description: str
    owner: User
    posts: List[Post]
