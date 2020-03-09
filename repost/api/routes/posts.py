"""Router for posts in respective resubs.

All of the posts endpoints are prefixed under a specific resub, and as
such every endpoint must resolve a resub. This is implemented in the
resolvers in `repost.resolvers`.
"""

from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, \
    HTTP_201_CREATED

from repost import crud, models
from repost.api.resolvers import resolve_post, resolve_user_owned_post, resolve_post_for_post_owner_or_resub_owner, \
    resolve_current_user, get_db
from repost.api.schemas import ErrorResponse, Post, EditPost, Comment, CreateComment

router = APIRouter()


@router.get('/{post_id}', response_model=Post,
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_post(post: models.Post = Depends(resolve_post)):
    """Get a specific post in a resub."""
    return post


@router.delete('/{post_id}',
               responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                          HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                          HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_post(post: models.Post = Depends(resolve_post_for_post_owner_or_resub_owner),
                      db: Session = Depends(get_db)):
    """Delete a post in a resub.

    Only the author of a post or the owner of the parent resub can
    delete the post.
    """
    crud.delete_post(db, post_id=post.id)


@router.patch('/{post_id}', response_model=Post,
              responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_post(*, post: models.Post = Depends(resolve_user_owned_post), edited_post: EditPost,
                    db: Session = Depends(get_db)):
    """Edit a post in a resub.

    Only the author of a post can edit the post."""
    return crud.update_post(db, post_id=post.id, **edited_post.dict(exclude_unset=True))


@router.patch('/{post_id}/vote/{vote}', response_model=Post,
              responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def vote_post(*, post: models.Post = Depends(resolve_post), vote: int = Path(..., ge=-1, le=1),
                    current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Vote on a post in a resub."""
    return crud.vote_post(db, post_id=post.id, author_id=current_user.id, vote=vote)


@router.get('/{post_id}/comments', response_model=List[Comment],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_comments_in_post(post: models.Post = Depends(resolve_post), db: Session = Depends(get_db)):
    """Get all comments in post."""
    return crud.get_comments(db, post.id)


@router.post('/{post_id}/comments', response_model=Comment, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_comment_in_post(*, post: models.Post = Depends(resolve_post), created_comment: CreateComment,
                                 current_user: models.User = Depends(resolve_current_user),
                                 db: Session = Depends(get_db)):
    """Create a comment in a post."""
    return crud.create_comment(db, author_id=current_user.id, parent_resub_id=post.parent_resub_id,
                               parent_post_id=post.id, parent_comment_id=None, content=created_comment.content)
