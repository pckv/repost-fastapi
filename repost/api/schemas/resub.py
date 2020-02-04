from pydantic import BaseModel

from .user import User


class Resub(BaseModel):
    """ The Resub schema to be returned as a response from the API. """
    name: str
    description: str
    owner: User
