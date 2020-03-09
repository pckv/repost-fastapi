"""Router for comments in respective posts.

All of the comments endpoints are prefixed under a specific resub and
post, and as such every endpoint must resolve both a resub and a post.
This is implemented in the resolvers in `repost.resolvers`.
"""

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, \
    HTTP_201_CREATED

from repost import models, crud
from repost.api.resolvers import resolve_comment_for_comment_owner_or_resub_owner, resolve_comment, \
    resolve_user_owned_comment, resolve_current_user, get_db
from repost.api.schemas import Comment, ErrorResponse, CreateComment, EditComment

router = APIRouter()


@router.post('/{comment_id}', response_model=Comment, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_reply(*, comment: models.Comment = Depends(resolve_comment), created_comment: CreateComment,
                       current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Create a reply to a comment in a post."""
    return crud.create_comment(db, author_id=current_user.id, parent_resub_id=comment.parent_resub_id,
                               parent_post_id=comment.parent_post_id, parent_comment_id=comment.id,
                               content=created_comment.content)


@router.delete('/{comment_id}',
               responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                          HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                          HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                          HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def delete_comment(comment: models.Comment = Depends(resolve_comment_for_comment_owner_or_resub_owner),
                         db: Session = Depends(get_db)):
    """Delete a comment in a post.

    Only the author of a comment or the owner of a resub can delete
    the comment.
    """
    crud.delete_comment(db, comment.id)


@router.patch('/{comment_id}', response_model=Comment,
              responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         HTTP_403_FORBIDDEN: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def edit_comment(*, comment: models.Comment = Depends(resolve_user_owned_comment), edited_comment: EditComment,
                       db: Session = Depends(get_db)):
    """Edit a comment in a post.

    Only the author of a comment can edit the comment.
    """
    return crud.update_comment(db, comment_id=comment.id, **edited_comment.dict(exclude_unset=True))


@router.patch('/{comment_id}/vote/{vote}', response_model=Comment,
              responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def vote_comment(*, comment: models.Comment = Depends(resolve_comment), vote: int = Path(..., ge=-1, le=1),
                       current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Vote on a comment in a post."""
    return crud.vote_comment(db, comment_id=comment.id, author_id=current_user.id, vote=vote)
