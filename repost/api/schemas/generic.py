import operator
from enum import Enum
from typing import Type

from pydantic.utils import GetterDict


class Vote(str, Enum):
    """Schema for voting paths."""
    upvote = 'upvote'
    downvote = 'downvote'
    novote = 'novote'


def bind_orm_fields(**fields: str) -> Type[GetterDict]:
    """GetterDict that binds ORM attributes to a Pydantic model.

    A field is a key-value mapping where the key is the name of the
    field in the Pydantic model, and the value is a string
    representation of the attribute to map it to.

    Example: bind_orm_fields(owner_username='owner.username')

    This would bind the Pydantic model's owner_username to the
    database model's owner.username.
    """

    class FieldBinder(GetterDict):
        """GetterDict for setting the owner_username attribute.

        Apply this to schemas that need to resolve owner_username from an
        ORM owner relationship.
        """

        def __init__(self, obj):
            for field, value in fields.items():
                setattr(obj, field, operator.attrgetter(value)(obj))

            super(FieldBinder, self).__init__(obj)

    return FieldBinder
