import operator
from typing import Type, Union, Callable, Any

from pydantic.utils import GetterDict


def bind_orm_fields(**fields: Union[str, Callable]) -> Type[GetterDict]:
    """GetterDict that binds ORM attributes to a Pydantic model.

    A field is a key-value mapping where the key is the name of the
    field in the Pydantic model, and the value is a string
    representation of the attribute to map it to.

    Example: bind_orm_fields(owner_username='owner.username')

    This would bind the Pydantic model's owner_username field to the
    database model's owner.username.

    The value can also be a function with a parameter for the ORM
    model. This function will be called and the returned value
    will be applied to the Pydantic model.

    Example: bind_orm_fields(votes=lambda obj: sum(v.vote for v in obj.votes))

    This would bind the Pydantic model's votes field to the sum of all
    elements in the database model's votes list.
    """

    class FieldBinder(GetterDict):
        """GetterDict for resolving attributes from the ORM model.

        Apply this to schemas that need to resolve inner attributes
        from ORM objects, or needs to run a method to resolve any
        given attribute.
        """

        def __init__(self, obj):
            self.custom_fields = {}
            for field, value in fields.items():
                if type(value) is str:
                    self.custom_fields[field] = operator.attrgetter(value)(obj)
                else:
                    self.custom_fields[field] = value(obj)

            super().__init__(obj)

        def get(self, key: Any, default: Any = None) -> Any:
            if key in self.custom_fields:
                return self.custom_fields[key]
            else:
                return super().get(key, default)

        def __getitem__(self, key: str) -> Any:
            if key in self.custom_fields:
                return self.custom_fields[key]
            else:
                return super().__getitem__(key)

    return FieldBinder
