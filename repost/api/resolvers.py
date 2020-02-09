"""Dependencies for resolving and verifying paths and ownership."""

from fastapi import Path, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from repost import crud
from repost.api.schemas import Resub, User, Post, Comment
from repost.api.security import authorize_user
from repost.database import SessionLocal


def get_db():
    """Dependency for database connections."""
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def resolve_user(db: Session = Depends(get_db), username: str = Path(...)) -> User:
    """Verify the user from path parameter.

    Base path: /users/{username}
    """
    db_user = crud.get_user(db, username=username)
    if not db_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User \'{username}\' not found')

    return User.from_orm(db_user)


async def resolve_current_user(db: Session = Depends(get_db), username: str = Depends(authorize_user)) -> User:
    """Resolve the currently authorized User."""
    return resolve_user(db, username)


async def resolve_resub(resub: str = Path(...)) -> Resub:
    """Verify the resub from path parameter.

    Base path: /resubs/{resub}
    """
    pass


async def resolve_user_owned_resub(resub: Resub = Depends(resolve_resub),
                                   current_user: User = Depends(resolve_current_user)) -> Resub:
    """Verify that the authorized user owns the resub before returning.

    Base path: /resubs/{resub}
    """
    pass


async def resolve_post(resub: Resub = Depends(resolve_resub),
                       post_id: int = Path(...)) -> Post:
    """Resolve the post from the path parameter.

    Base path: /resubs/{resub}/posts/{post_id}
    """
    pass


async def resolve_user_owned_post(post: Post = Depends(resolve_post),
                                  current_user: User = Depends(resolve_current_user)) -> Post:
    """Verify that the authorized user owns the post before returning.

    Base path: /resubs/{resub}/posts/{post_id}
    """
    pass


async def resolve_post_for_post_owner_or_resub_owner(resub: Resub = Depends(resolve_resub),
                                                     post: Post = Depends(resolve_post),
                                                     current_user: User = Depends(resolve_current_user)) -> Post:
    """Verify that the authorized user owns the post or owns the resub before returning.

    Base path: /resubs/{resub}/posts/{post_id}
    """
    pass


async def resolve_comment(post: Post = Depends(resolve_post),
                          comment_id: int = Path(...)) -> Comment:
    """ Resolve the comment from the path parameter. """
    pass


async def resolve_user_owned_comment(post: Comment = Depends(resolve_comment),
                                     current_user: User = Depends(resolve_current_user)) -> Post:
    """ Verify that the authorized user owns the comment before returning. """
    pass


async def resolve_comment_for_comment_owner_or_resub_owner(resub: Resub = Depends(resolve_resub),
                                                           comment: Comment = Depends(resolve_comment),
                                                           current_user: User = Depends(
                                                               resolve_current_user)) -> Comment:
    """ Verify that the authorized user owns the comment or owns the resub before returning. """
    pass
