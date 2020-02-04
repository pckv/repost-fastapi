from typing import List

from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from repost.api.schemas import User, UserCreate, Resub, Post, Comment

router = APIRouter()


@router.post('/', response_model=User, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'description': 'Username taken'}})
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


@router.get('/{username}', response_model=User,
            responses={HTTP_404_NOT_FOUND: {'description': 'User not found'}})
async def get_user(username: str):
    """ """
    pass


@router.get('/{username}/resubs', response_model=List[Resub])
async def get_resubs_owned_by_user(username: str):
    """ """
    pass


@router.get('/{username}/posts', response_model=List[Post])
async def get_posts_by_user(username: str):
    """ """
    pass


@router.get('/{username}/comments', response_model=List[Comment])
async def get_comments_by_user(username: str):
    """ """
    pass
