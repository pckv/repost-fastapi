"""Posts endpoints"""


from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from repost.api.resolvers import resolve_resub, resolve_post
from repost.api.schemas import ErrorResponse, User, Resub
from repost.api.schemas.post import CreatePost, Post
from repost.api.security import get_current_user

router = APIRouter()


@router.get('/', response_model=List[Post],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_posts(resub: Resub = Depends(resolve_resub)):
    """Get posts"""
    pass


@router.post('/', response_model=Post,
             responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_post(*, resub: Resub = Depends(resolve_resub),
                      post: CreatePost, user: User = Depends(get_current_user),):
    """Create new post"""
    pass


@router.get('/{post_id}', response_model=Post,
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_post(post: Post = Depends(resolve_post)):
    pass


@router.delete('/{post_id}',
               responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_post(post: Post = Depends(resolve_post), user: User = Depends(get_current_user)):
    """Delete post"""
    pass


@router.patch('/{post_id}', response_model=Post,
              responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_post(post: Post = Depends(resolve_post), user: User = Depends(get_current_user)):
    """Edit post"""
    pass
