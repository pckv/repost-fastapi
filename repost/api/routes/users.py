"""Router for user accounts."""

from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from repost.api.schemas import User, CreateUser, Resub, Post, Comment, ErrorResponse
from repost.api.security import get_current_user

router = APIRouter()


@router.post('/', response_model=User, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'description': 'Username taken', 'model': ErrorResponse}})
async def create_user(user: CreateUser):
    """ """
    pass


@router.get('/me', response_model=User,
            responses={HTTP_403_FORBIDDEN: {'description': 'Invalid authorization', 'model': ErrorResponse}})
async def get_current_user(current_user: User = Depends(get_current_user)):
    """ """
    pass


@router.patch('/me', response_model=User,
              responses={HTTP_403_FORBIDDEN: {'description': 'Invalid authorization', 'model': ErrorResponse}})
async def edit_current_user(current_user: User = Depends(get_current_user)):  # TODO: Finish endpoint
    """ """
    pass


@router.delete('/me',
               responses={HTTP_403_FORBIDDEN: {'description': 'Invalid authorization', 'model': ErrorResponse}})
async def delete_current_user(current_user: User = Depends(get_current_user)):
    """ """
    pass


@router.get('/{username}', response_model=User,
            responses={HTTP_404_NOT_FOUND: {'description': 'User not found', 'model': ErrorResponse}})
async def get_user(username: str):
    """ """
    pass


@router.get('/{username}/resubs', response_model=List[Resub],
            responses={HTTP_404_NOT_FOUND: {'description': 'User not found', 'model': ErrorResponse}})
async def get_resubs_owned_by_user(username: str):
    """ """
    pass


@router.get('/{username}/posts', response_model=List[Post],
            responses={HTTP_404_NOT_FOUND: {'description': 'User not found', 'model': ErrorResponse}})
async def get_posts_by_user(username: str):
    """ """
    pass


@router.get('/{username}/comments', response_model=List[Comment],
            responses={HTTP_404_NOT_FOUND: {'description': 'User not found', 'model': ErrorResponse}})
async def get_comments_by_user(username: str):
    """ """
    pass
