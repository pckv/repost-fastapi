from sqlalchemy.orm import Session

from repost.api.schemas import CreateUser, EditUser
from repost.models import User
from repost.password import hash_password


def get_user(db: Session, *, username: str) -> User:
    """Get the user with the given username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, *, user: CreateUser) -> User:
    """Create a new user in the database."""
    db_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()

    db.refresh(db_user)
    return db_user


def update_user(db: Session, *, username: str, user: EditUser) -> User:
    """Edit the user with the given username."""
    db.query(User).filter(User.username == username).update(user.dict(exclude_unset=True))
    db.commit()

    return get_user(db, username=username)


def delete_user(db: Session, *, username: str):
    """Delete the user with the given username."""
    db.query(User).filter(User.username == username).delete()
    db.commit()
