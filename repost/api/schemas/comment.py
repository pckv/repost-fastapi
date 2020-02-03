from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel

from repost.api.schemas import Post, User


class Comment(BaseModel):
    """ The Comment schema to be returned as a response from the API. """
    id: str
    parent: Union[Post, 'Comment']
    content: str
    author: User
    created: datetime
    edited: Optional[datetime]
    votes: int
