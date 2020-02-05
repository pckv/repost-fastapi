from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from repost.api.resolvers import resolve_post, resolve_comment_for_comment_owner_or_resub_owner, resolve_comment, \
    resolve_user_owned_comment
from repost.api.schemas import Comment, Post, User, ErrorResponse
from repost.api.schemas.comment import CreateComment, Vote, EditComment
from repost.api.security import get_current_user

router = APIRouter()


@router.get('/', response_model=List[Comment],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_comments(post: Post = Depends(resolve_post)):
    """Get all comments from post"""
    pass


@router.post('/', response_model=Comment,
             responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_comment(*, post: Post = Depends(resolve_post), comment: CreateComment,
                         current_user: User = Depends(get_current_user)):
    """Create comment"""
    pass


@router.delete('/{comment_id}',
               responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_comment(comment: Comment = Depends(resolve_comment_for_comment_owner_or_resub_owner)):
    """Delete a comment"""
    pass


@router.patch('/{comment_id}', response_model=Comment,
              responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_comment(*, comment: Comment = Depends(resolve_user_owned_comment), edited_comment: EditComment):
    """Edit a comment"""
    pass


@router.patch('/{comment_id}/{vote}', response_model=Comment,
              responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def vote_comment(*, comment: Comment = Depends(resolve_comment), vote: Vote,
                       current_user: User = Depends(get_current_user)):
    """Vote on a comment"""
    pass


@router.post('/{comment_id}/', response_model=Comment,
             responses={HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_reply(*, comment: Comment = Depends(resolve_comment), reply: CreateComment,
                       current_user: User = Depends(get_current_user)):
    """Create a reply to a comment"""
    pass

