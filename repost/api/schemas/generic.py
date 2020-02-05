from enum import Enum


class Vote(str, Enum):
    """Schema for voting paths"""
    upvote = 'upvote'
    downvote = 'downvote'
    novote = 'novote'
