from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel

from .user import User


class Post(BaseModel):
    """ The Post schema to be returned as a response from the API. """
    id: int
    parent_id: int = Field(..., description='ID of the post\'s parent resub')
    title: str
    url: Optional[str]
    content: Optional[str]
    author: User
    created: datetime
    edited: Optional[datetime]
    votes: int
