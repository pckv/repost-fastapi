from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from repost.api.resolvers import resolve_resub, resolve_user_owned_resub
from repost.api.schemas import User, Resub, CreateResub, EditResub, ErrorResponse
from repost.api.security import get_current_user

router = APIRouter()


@router.get('/', response_model=List[Resub])
async def get_resubs():
    """ """
    pass


@router.post('/', response_model=Resub,
             responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse}})
async def create_resub(resub: CreateResub, current_user: User = Depends(get_current_user)):
    """ """
    pass


@router.get('/{resub}', response_model=Resub,
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_resub(resub: Resub = Depends(resolve_resub)):
    """ """
    pass


@router.patch('/{resub}', response_model=Resub,
              responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_resub(*, resub: Resub = Depends(resolve_user_owned_resub), edited_resub: EditResub):
    """ """
    pass


@router.delete('/{resub}',
               responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_resub(resub: Resub = Depends(resolve_user_owned_resub)):
    """ """
    pass

