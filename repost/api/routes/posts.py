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
from repost.api.resolvers import resolve_resub, resolve_post, resolve_user_owned_post, \
    resolve_post_for_post_owner_or_resub_owner, resolve_current_user, get_db
from repost.api.schemas import ErrorResponse, CreatePost, Post, EditPost

router = APIRouter()


@router.get('/', response_model=List[Post],
            responses={HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def get_posts(resub: models.Resub = Depends(resolve_resub), db: Session = Depends(get_db)) -> List[models.Post]:
    """Get all posts in a resub."""
    return crud.get_posts(db, parent_resub_id=resub.id)


@router.post('/', response_model=Post, status_code=HTTP_201_CREATED,
             responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                        HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                        HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def create_post(*, resub: models.Resub = Depends(resolve_resub),
                      post: CreatePost, current_user: models.User = Depends(resolve_current_user),
                      db: Session = Depends(get_db)) -> models.Post:
    """Create a new post in a resub."""
    post = crud.create_post(db, author_id=current_user.id, parent_resub_id=resub.id, title=post.title, url=post.url,
                            content=post.content)

    return post


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


@router.patch('/{post_id}/{vote}', response_model=Post,
              responses={HTTP_400_BAD_REQUEST: {'model': ErrorResponse},
                         HTTP_401_UNAUTHORIZED: {'model': ErrorResponse},
                         HTTP_404_NOT_FOUND: {'model': ErrorResponse}})
async def vote_post(*, post: models.Post = Depends(resolve_post), vote: int = Path(..., ge=-1, le=1),
                    current_user: models.User = Depends(resolve_current_user), db: Session = Depends(get_db)):
    """Vote on a post in a resub."""
    return crud.vote_post(db, post_id=post.id, author_id=current_user.id, vote=vote)
