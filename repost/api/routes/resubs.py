from typing import List

from fastapi import APIRouter, Depends

from repost.api.resolvers import resolve_resub, resolve_user_owned_resub
from repost.api.schemas import User, Resub, CreateResub, EditResub
from repost.api.security import get_current_user

router = APIRouter()


@router.get('/', response_model=List[Resub])
async def get_resubs():
    """ """
    pass


@router.post('/', response_model=Resub)
async def create_resub(resub: CreateResub, current_user: User = Depends(get_current_user)):
    """ """
    pass


@router.get('/{resub}', response_model=Resub)
async def get_resub(resub: Resub = Depends(resolve_resub)):
    """ """
    pass


@router.patch('/{resub}', response_model=Resub)
async def edit_resub(*, resub: Resub = Depends(resolve_user_owned_resub), edited_resub: EditResub):
    """ """
    pass


@router.delete('/{resub}')
async def delete_resub(resub: Resub = Depends(resolve_user_owned_resub)):
    """ """
    pass

