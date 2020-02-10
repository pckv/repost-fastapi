"""Router for dealing with resubs.

A resub is a user-created community, where fans can create related
posts.
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from repost import crud, models
from repost.api.resolvers import resolve_resub, resolve_user_owned_resub, resolve_current_user, get_db, resolve_user
from repost.api.schemas import Resub, CreateResub, EditResub, ErrorResponse

router = APIRouter()


@router.get('/', response_model=List[Resub])
async def get_resubs(db: Session = Depends(get_db)):
    """Get all resubs."""
    return crud.get_resubs(db)


@router.post('/', response_model=Resub,
             responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        HTTP_403_FORBIDDEN: {'model': ErrorResponse}})
async def create_resub(resub: CreateResub, current_user: models.User = Depends(resolve_current_user),
                       db: Session = Depends(get_db)):
    """Create a new resub."""
    resub = crud.create_resub(db, owner_id=current_user.id, name=resub.name, description=resub.description)

    return resub


@router.get('/{resub}', response_model=Resub,
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_resub(resub: models.Resub = Depends(resolve_resub)):
    """Get a specific resub."""
    return resub


@router.delete('/{resub}',
               responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_resub(resub: models.Resub = Depends(resolve_user_owned_resub), db: Session = Depends(get_db)):
    """Delete a resub.

    Only the owner of a resub can delete the resub.
    """
    crud.delete_resub(db, name=resub.name)


@router.patch('/{resub}', response_model=Resub,
              responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
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
