from typing import Any, List

from sqlalchemy.orm import Session

from repost.models import User, Comment, Post, Resub
from repost.password import hash_password


def get_user(db: Session, *, username: str) -> User:
    """Get the user with the given username."""
    return db.query(User).filter_by(username=username).first()


def create_user(db: Session, *, username: str, password: str) -> User:
    """Create a new user in the database."""
    db_user = User(username=username, hashed_password=hash_password(password))
    db.add(db_user)
    db.commit()

    db.refresh(db_user)
    return db_user


def update_user(db: Session, *, username: str, **columns: Any) -> User:
    """Edit the user with the given username.

    Enter any `repost.models.User` column to update in `**columns`.
    """
    db.query(User).filter_by(username=username).update(columns)
    db.commit()

    return get_user(db, username=username)


def delete_user(db: Session, *, username: str):
    """Delete the user with the given username."""
    db.query(User).filter_by(username=username).delete()
    db.commit()


def get_resubs_by_user(db: Session, user_id: int) -> List[Resub]:
    """Get all resubs by a user with the specified ID."""
    return db.query(Resub).filter_by(owner_id=user_id).all()


def get_posts_by_user(db: Session, user_id: int) -> List[Post]:
    """Get all posts by a user with the specified ID."""
    return db.query(Post).filter_by(author_id=user_id).all()


def get_comments_by_user(db: Session, user_id: int) -> List[Comment]:
    """Get all comments by a user with the specified ID."""
    return db.query(Comment).filter_by(author_id=user_id).all()
