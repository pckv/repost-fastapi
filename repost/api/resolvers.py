"""Dependencies for resolving and verifying paths and ownership."""

from fastapi import Path, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session

from repost import crud
from repost import models
from repost.api.security import authorize_user
from repost.database import SessionLocal


def get_db():
    """Dependency for database connections."""
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def resolve_user(username: str = Path(...), db: Session = Depends(get_db)) -> models.User:
    """Verify the user from path parameter.

    Base path: /users/{username}
    """
    db_user = crud.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User \'{username}\' not found')

    return db_user


async def resolve_current_user(username: str = Security(authorize_user, scopes=['user']),
                               db: Session = Depends(get_db)) -> models.User:
    """Resolve the currently authorized User."""
    db_user = crud.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'The owner of this JSON Web Token no longer exists')

    return db_user


async def resolve_resub(resub: str = Path(...), db: Session = Depends(get_db)) -> models.Resub:
    """Verify the resub from path parameter."""
    db_resub = crud.get_resub(db, name=resub)
    if not db_resub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Resub \'{resub}\' not found')

    return db_resub


async def resolve_user_owned_resub(resub: models.Resub = Depends(resolve_resub),
                                   current_user: models.User = Depends(resolve_current_user)) -> models.Resub:
    """Verify that the authorized user owns the resub before returning."""
    if resub.owner != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the owner of this resub')

    return resub


async def resolve_post(post_id: int = Path(...), db: Session = Depends(get_db)) -> models.Post:
    """Resolve the post from the path parameter."""
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post \'{post_id}\' not found')

    return db_post


async def resolve_user_owned_post(post: models.Post = Depends(resolve_post),
                                  current_user: models.User = Depends(resolve_current_user)) -> models.Post:
    """Verify that the authorized user owns the post before returning."""
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of this post')

    return post


async def resolve_post_for_post_owner_or_resub_owner(post: models.Post = Depends(resolve_post),
                                                     current_user: models.User = Depends(
                                                         resolve_current_user)) -> models.Post:
    """Verify that the authorized user owns the post or owns the resub before returning."""
    if current_user not in (post.author, post.parent_resub.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not the author of this post or the owner of this resub')

    return post


async def resolve_comment(comment_id: int = Path(...), db: Session = Depends(get_db)) -> models.Comment:
    """ Resolve the comment from the path parameter. """
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Comment \'{comment_id}\' not found')

    return db_comment


async def resolve_user_owned_comment(comment: models.Comment = Depends(resolve_comment),
                                     current_user: models.User = Depends(resolve_current_user)) -> models.Comment:
    """ Verify that the authorized user owns the comment before returning. """
    if comment.author != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of this comment')

    return comment


async def resolve_comment_for_comment_owner_or_resub_owner(comment: models.Comment = Depends(resolve_comment),
                                                           current_user: models.User = Depends(
                                                               resolve_current_user)) -> models.Comment:
    """ Verify that the authorized user owns the comment or owns the resub before returning. """
    if current_user not in (comment.author, comment.parent_resub.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not the author of this comment or the owner of this resub')

    return comment
