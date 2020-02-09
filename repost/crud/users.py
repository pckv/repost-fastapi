from typing import Any

from sqlalchemy.orm import Session

from repost import models
from repost.password import hash_password


def get_user(db: Session, *, username: str) -> models.User:
    """Get the user with the given username."""
    return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, *, username: str, password: str) -> models.User:
    """Create a new user in the database."""
    db_user = models.User(username=username, hashed_password=hash_password(password))
    db.add(db_user)
    db.commit()

    db.refresh(db_user)
    return db_user


def update_user(db: Session, *, username: str, **columns: Any) -> models.User:
    """Edit the user with the given username.

    Enter any `repost.models.User` column to update in `**columns`.
    """
    db.query(models.User).filter_by(username=username).update(columns)
    db.commit()

    return get_user(db, username=username)


def delete_user(db: Session, *, username: str):
    """Delete the user with the given username."""
    db.query(models.User).filter_by(username=username).delete()
    db.commit()
