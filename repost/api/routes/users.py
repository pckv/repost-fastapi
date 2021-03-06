"""Router for user accounts."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from repost import crud, models
from repost.api.resolvers import resolve_user, get_db, resolve_current_user
from repost.api.schemas import User, CreateUser, Resub, Post, Comment, ErrorResponse, EditUser

router = APIRouter()


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse}})
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    """Create a new user."""
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User \'{user.username}\' already exists')

    return crud.create_user(db, username=user.username, password=user.password)


@router.get('/me', response_model=User,
            responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                       status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse}})
async def get_current_user(current_user: models.User = Depends(resolve_current_user)):
    """Get the currently authorized user."""
    return current_user


@router.patch('/me', response_model=User,
              responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse}})
async def edit_current_user(*, current_user: models.User = Depends(get_current_user), edited_user: EditUser,
                            db: Session = Depends(get_db)):
    """Edit the currently authorized user."""
    return crud.update_user(db, username=current_user.username, **edited_user.dict(exclude_unset=True))


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT,
               responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                          status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse}})
async def delete_current_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete the currently authorized user."""
    crud.delete_user(db, username=current_user.username)


@router.get('/{username}', response_model=User,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_user(user: models.User = Depends(resolve_user)):
    """Get a specific user."""
    return user


@router.get('/{username}/resubs', response_model=List[Resub],
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_resubs_owned_by_user(user: models.User = Depends(resolve_user), db: Session = Depends(get_db),
                                   page: int = 0, page_size: int = 100):
    """Get all resubs owned by a specific user."""
    return crud.get_resubs_by_user(db, user_id=user.id, offset=page * page_size, limit=page_size)


@router.get('/{username}/posts', response_model=List[Post],
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_posts_by_user(user: models.User = Depends(resolve_user), db: Session = Depends(get_db),
                            page: int = 0, page_size: int = 100):
    """Get all posts by a specific user."""
    return crud.get_posts_by_user(db, user_id=user.id, offset=page * page_size, limit=page_size)


@router.get('/{username}/comments', response_model=List[Comment],
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_comments_by_user(user: models.User = Depends(resolve_user), db: Session = Depends(get_db),
                               page: int = 0, page_size: int = 100):
    """Get all comments by a specific user."""
    return crud.get_comments_by_user(db, user_id=user.id, offset=page * page_size, limit=page_size)
