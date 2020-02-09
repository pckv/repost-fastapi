from enum import Enum

from pydantic.utils import GetterDict


class Vote(str, Enum):
    """Schema for voting paths"""
    upvote = 'upvote'
    downvote = 'downvote'
    novote = 'novote'


class SetOwnerUsername(GetterDict):
    def __init__(self, obj):
        obj.owner_username = obj.owner.username
        super(SetOwnerUsername, self).__init__(obj)
