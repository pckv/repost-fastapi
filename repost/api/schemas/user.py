from typing import Optional, List

from pydantic import BaseModel

from repost.api.schemas import Resub, Post, Comment


class User(BaseModel):
    username: str
    bio: str
    avatar_url: Optional[str]
    resubs: List[Resub]
    posts: List[Post]
    comments: List[Comment]
