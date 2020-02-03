from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .user import User


class Comment(BaseModel):
    """ The Comment schema to be returned as a response from the API. """
    id: int
    parent_id: int = Field(..., description='ID of the comment\'s parent post or comment')
    content: str
    author: User
    created: datetime
    edited: Optional[datetime]
    votes: int
