from typing import List, Any

from sqlalchemy.orm import Session

from repost.models import Comment


def get_comments(db: Session, post_id: int) -> List[Comment]:
    """Get all comments in a post with the speficied ID."""
    return db.query(Comment).filter_by(parent_post_id=post_id).all()


def get_comment(db: Session, comment_id: int) -> Comment:
    """Get a comment with the the specified ID."""
    return db.query(Comment).filter_by(id=comment_id).first()


def create_comment(db: Session, *, author_id: int, parent_post_id: int, parent_resub_id: int,
                   parent_comment_id: int = None, content: str) -> Comment:
    """Create a new comment with the specified parent resub, post and comment."""
    db_comment = Comment(author_id=author_id, parent_post_id=parent_post_id, parent_comment_id=parent_comment_id,
                         parent_resub_id=parent_resub_id, content=content)
    db.add(db_comment)

    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    """Delete the comment with the given ID."""
    db.query(Comment).filter_by(id=comment_id).delete()
    db.commit()


def update_comment(db: Session, comment_id: int, **columns: Any) -> Comment:
    """Update the comment with the given ID.

    Enter any `repost.models.Comment` column to update in `**columns`.
    """
    db.query(Comment).filter_by(id=comment_id).update(columns)
    db.commit()

    return get_comment(db, comment_id=comment_id)
