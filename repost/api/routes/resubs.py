"""Router for dealing with resubs.

A resub is a user-created community, where fans can create related
posts.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from repost import crud, models
from repost.api.resolvers import resolve_resub, resolve_user_owned_resub, resolve_current_user, get_db, resolve_user
from repost.api.schemas import Resub, CreateResub, EditResub, ErrorResponse, Post, CreatePost

router = APIRouter()


@router.get('/', response_model=List[Resub])
async def get_resubs(db: Session = Depends(get_db)):
    """Get all resubs."""
    return crud.get_resubs(db)


@router.post('/', response_model=Resub, status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse}})
async def create_resub(resub: CreateResub, current_user: models.User = Depends(resolve_current_user),
                       db: Session = Depends(get_db)):
    """Create a new resub."""
    db_resub = crud.get_resub(db, name=resub.name)
    if db_resub:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Resub \'{resub.name}\' already exists')

    return crud.create_resub(db, owner_id=current_user.id, name=resub.name, description=resub.description)


@router.get('/{resub}', response_model=Resub,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_resub(resub: models.Resub = Depends(resolve_resub)):
    """Get a specific resub."""
    return resub


@router.delete('/{resub}',
               responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                          status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                          status.HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_resub(resub: models.Resub = Depends(resolve_user_owned_resub), db: Session = Depends(get_db)):
    """Delete a resub.

    Only the owner of a resub can delete the resub.
    """
    crud.delete_resub(db, name=resub.name)


@router.patch('/{resub}', response_model=Resub,
              responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         status.HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_resub(*, resub: models.Resub = Depends(resolve_user_owned_resub), edited_resub: EditResub,
                     db: Session = Depends(get_db)):
    """Edit a resub.

    Only the owner of a resub can delete the resub.
    """
    updated = edited_resub.dict(exclude_unset=True)

    # Replace new owner's username with the new owner's id
    if 'new_owner_username' in updated:
        db_user = resolve_user(updated.pop('new_owner_username'), db)
        updated['owner_id'] = db_user.id

    return crud.update_resub(db, name=resub.name, **updated)


@router.get('/{resub}/posts', response_model=List[Post],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_posts_in_resub(resub: models.Resub = Depends(resolve_resub), db: Session = Depends(get_db)):
    """Get all posts in a resub."""
    return crud.get_posts(db, parent_resub_id=resub.id)


@router.post('/{resub}/posts', response_model=Post, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_post_in_resub(*, resub: models.Resub = Depends(resolve_resub),
                               post: CreatePost, current_user: models.User = Depends(resolve_current_user),
                               db: Session = Depends(get_db)):
    """Create a new post in a resub."""
    post = crud.create_post(db, author_id=current_user.id, parent_resub_id=resub.id, title=post.title, url=post.url,
                            content=post.content)

    return post
