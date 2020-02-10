from typing import Optional, Any, List

from sqlalchemy.orm import Session

from repost.models import Post


def get_posts(db: Session, *, parent_resub_id: int) -> List[Post]:
    """Get all posts in a resub."""
    return db.query(Post).filter_by(parent_resub_id=parent_resub_id).all()


def get_post(db: Session, *, post_id: int) -> Optional[Post]:
    """Get the post with the given ID."""
    return db.query(Post).filter_by(id=post_id).first()


def create_post(db: Session, *, author_id: int, parent_resub_id: int, title: str, url: str = None,
                content: str = None) -> Post:
    """Create a new post with the specified owner."""
    db_post = Post(author_id=author_id, parent_resub_id=parent_resub_id, title=title, url=url, content=content)
    db.add(db_post)

    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, *, post_id: int, **columns: Any):
    """Update the post with the given ID.

    Enter any `repost.models.Post` column to update in `**columns`.
    """
    db.query(Post).filter_by(id=post_id).update(columns)
    db.commit()

    return get_post(db, post_id=post_id)


def delete_post(db: Session, *, post_id: int):
    """Delete the post with the given ID."""
    db.query(Post).filter_by(id=post_id).delete()
    db.commit()
