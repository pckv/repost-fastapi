from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel

from repost.api.schemas import Post, User


class Comment(BaseModel):
    id: str
    parent: Union[Post, 'Comment']
    content: str
    author: User
    created: datetime
    edited: Optional[datetime]
    votes: int
