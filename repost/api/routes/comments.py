"""Router for comments in respective posts.

All of the comments endpoints are prefixed under a specific resub and
post, and as such every endpoint must resolve both a resub and a post.
This is implemented in the resolvers in `repost.resolvers`.
"""

from typing import List

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from repost import models, crud
from repost.api.resolvers import resolve_post, resolve_comment_for_comment_owner_or_resub_owner, resolve_comment, \
    resolve_user_owned_comment, resolve_current_user, get_db
from repost.api.schemas import Comment, ErrorResponse, CreateComment, EditComment

router = APIRouter()


@router.get('/', response_model=List[Comment],
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_comments(post: models.Post = Depends(resolve_post), db: Session = Depends(get_db)):
    """Get all comments in post."""
    return crud.get_comments(db, post.id)


@router.post('/', response_model=Comment, status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_comment(*, post: models.Post = Depends(resolve_post), created_comment: CreateComment,
                         current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Create a comment in a post."""
    return crud.create_comment(db, author_id=current_user.id, parent_resub_id=post.parent_resub_id,
                               parent_post_id=post.id, parent_comment_id=None, content=created_comment.content)


@router.post('/{comment_id}', response_model=Comment, status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_reply(*, comment: models.Comment = Depends(resolve_comment), created_comment: CreateComment,
                       current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Create a reply to a comment in a post."""
    return crud.create_comment(db, author_id=current_user.id, parent_resub_id=comment.parent_resub_id,
                               parent_post_id=comment.parent_post_id, parent_comment_id=comment.id,
                               content=created_comment.content)


@router.delete('/{comment_id}',
               responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                          status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                          status.HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_comment(comment: models.Comment = Depends(resolve_comment_for_comment_owner_or_resub_owner),
                         db: Session = Depends(get_db)):
    """Delete a comment in a post.

    Only the author of a comment or the owner of a resub can delete
    the comment.
    """
    crud.delete_comment(db, comment.id)


@router.patch('/{comment_id}', response_model=Comment,
              responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         status.HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_comment(*, comment: models.Comment = Depends(resolve_user_owned_comment), edited_comment: EditComment,
                       db: Session = Depends(get_db)):
    """Edit a comment in a post.

    Only the author of a comment can edit the comment.
    """
    return crud.update_comment(db, comment_id=comment.id, **edited_comment.dict(exclude_unset=True))


@router.patch('/{comment_id}/vote/{vote}', response_model=Comment,
              responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         status.HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def vote_comment(*, comment: models.Comment = Depends(resolve_comment), vote: int = Path(..., ge=-1, le=1),
                       current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Vote on a comment in a post."""
    return crud.vote_comment(db, comment_id=comment.id, author_id=current_user.id, vote=vote)
