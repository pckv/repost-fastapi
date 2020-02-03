from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from repost.api.schemas import Resub, User, Comment


class Post(BaseModel):
    id: int
    parent: Resub
    title: str
    url: Optional[str]
    content: Optional[str]
    author: User
    created: datetime
    edited: Optional[datetime]
    comments: List[Comment]
    votes: int
