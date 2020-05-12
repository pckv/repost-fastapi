from typing import Any, List, Optional

from sqlalchemy.orm import Session

from repost.models import Resub


def get_resubs(db: Session, offset: int = 0, limit: int = 100) -> List[Resub]:
    """Get all resubs."""
    return db.query(Resub).order_by(Resub.created.desc()).offset(offset).limit(limit).all()


def get_resub(db: Session, *, name: str) -> Optional[Resub]:
    """Get the resub with the given name."""
    return db.query(Resub).filter(Resub.name == name).first()


def create_resub(db: Session, *, owner_id: int, name: str, description: str) -> Resub:
    """Create a new resub with the specified owner."""
    db_resub = Resub(owner_id=owner_id, name=name, description=description)
    db.add(db_resub)

    db.commit()
    db.refresh(db_resub)
    return db_resub


def update_resub(db: Session, *, name: str, **columns: Any) -> Resub:
    """Update the resub with the given name.

    Enter any `repost.models.Resub` column to update in `**columns`.
    """
    db.query(Resub).filter(Resub.name == name).update(columns)
    db.commit()

    return get_resub(db, name=name)


def delete_resub(db: Session, *, name: str):
    """Delete the resub with the given name."""
    db.query(Resub).filter(Resub.name == name).delete()
    db.commit()
