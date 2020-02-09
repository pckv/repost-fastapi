"""Router for user accounts."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from repost import crud
from repost.api.resolvers import resolve_user, get_db, resolve_current_user
from repost.api.schemas import User, CreateUser, Resub, Post, Comment, ErrorResponse, EditUser

router = APIRouter()


@router.post('/', response_model=User, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse}})
async def create_user(*, db: Session = Depends(get_db), user: CreateUser):
    """Create a new user."""
    return crud.create_user(db, user=user)


@router.get('/me', response_model=User,
            responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse}})
async def get_current_user(current_user: User = Depends(resolve_current_user)):
    """Get the currently authorized user."""
    return current_user


@router.patch('/me', response_model=User,
              responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse}})
async def edit_current_user(*, current_user: User = Depends(get_current_user), edited_user: EditUser):
    """Edit the currently authorized user."""
    pass


@router.delete('/me',
               responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse}})
async def delete_current_user(current_user: User = Depends(get_current_user)):
    """Delete the currently authorized user."""
    pass


@router.get('/{username}', response_model=User,
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_user(user: User = Depends(resolve_user)):
    """Get a specific user."""
    return user


@router.get('/{username}/resubs', response_model=List[Resub],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_resubs_owned_by_user(user: User = Depends(resolve_user)):
    """Get all resubs owned by a specific user."""
    pass


@router.get('/{username}/posts', response_model=List[Post],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_posts_by_user(user: User = Depends(resolve_user)):
    """Get all posts by a specific user."""
    pass


@router.get('/{username}/comments', response_model=List[Comment],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_comments_by_user(user: User = Depends(resolve_user)):
    """Get all comments by a specific user."""
    pass
