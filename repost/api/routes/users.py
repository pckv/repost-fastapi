from fastapi import APIRouter, Path, Depends
from starlette.status import HTTP_201_CREATED

from repost.api.schemas import User, UserCreate

router = APIRouter()


@router.get('/{username}', response_model=User)
async def get_user(username: str):
    """ """
    pass


@router.post('/', response_model=User, status_code=HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """ """
    pass


@router.get('/me', response_model=User)
async def get_current_user(current_user: User):  # TODO: Create dependency
    """ """
    pass


@router.patch('/me', response_model=User)
async def edit_current_user(current_user: User):  # TODO: Finish endpoint
    """ """
    pass


@router.delete('/me')
async def delete_current_user(current_user: User):  # TODO: Create dependency
    """ """
    pass
