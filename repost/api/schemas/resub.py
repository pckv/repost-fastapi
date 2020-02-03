from typing import List

from pydantic import BaseModel

from repost.api.schemas import User, Post


class Resub(BaseModel):
    name: str
    description: str
    owner: User
    posts: List[Post]
