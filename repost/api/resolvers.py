"""Dependencies for resolving and verifying paths and ownership."""

from fastapi import Path, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

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
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User \'{username}\' not found')

    return db_user


async def resolve_current_user(username: str = Depends(authorize_user), db: Session = Depends(get_db)) -> models.User:
    """Resolve the currently authorized User."""
    return resolve_user(username, db)


async def resolve_resub(resub: str = Path(...), db: Session = Depends(get_db)) -> models.Resub:
    """Verify the resub from path parameter.

    Base path: /resubs/{resub}
    """
    db_resub = crud.get_resub(db, name=resub)
    if not db_resub:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Resub \'{resub}\' not found')

    return Resub.from_orm(db_resub)


async def resolve_user_owned_resub(resub: models.Resub = Depends(resolve_resub),
                                   current_user: models.User = Depends(resolve_current_user)) -> models.Resub:
    """Verify that the authorized user owns the resub before returning.

    Base path: /resubs/{resub}
    """
    pass


async def resolve_post(resub: models.Resub = Depends(resolve_resub),
                       post_id: int = Path(...)) -> models.Post:
    """Resolve the post from the path parameter.

    Base path: /resubs/{resub}/posts/{post_id}
    """
    pass


async def resolve_user_owned_post(post: models.Post = Depends(resolve_post),
                                  current_user: models.User = Depends(resolve_current_user)) -> models.Post:
    """Verify that the authorized user owns the post before returning.

    Base path: /resubs/{resub}/posts/{post_id}
    """
    pass


async def resolve_post_for_post_owner_or_resub_owner(resub: models.Resub = Depends(resolve_resub),
                                                     post: models.Post = Depends(resolve_post),
                                                     current_user: models.User = Depends(
                                                         resolve_current_user)) -> models.Post:
    """Verify that the authorized user owns the post or owns the resub before returning.

    Base path: /resubs/{resub}/posts/{post_id}
    """
    pass


async def resolve_comment(post: models.Post = Depends(resolve_post),
                          comment_id: int = Path(...)) -> models.Comment:
    """ Resolve the comment from the path parameter. """
    pass


async def resolve_user_owned_comment(post: models.Comment = Depends(resolve_comment),
                                     current_user: models.User = Depends(resolve_current_user)) -> models.Post:
    """ Verify that the authorized user owns the comment before returning. """
    pass


async def resolve_comment_for_comment_owner_or_resub_owner(resub: models.Resub = Depends(resolve_resub),
                                                           comment: models.Comment = Depends(resolve_comment),
                                                           current_user: models.User = Depends(
                                                               resolve_current_user)) -> models.Comment:
    """ Verify that the authorized user owns the comment or owns the resub before returning. """
    pass
