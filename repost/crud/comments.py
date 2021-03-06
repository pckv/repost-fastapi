from typing import List, Any

from sqlalchemy.orm import Session

from repost.models import Comment, CommentVote


def get_comments(db: Session, post_id: int, offset: int = 0, limit: int = 100) -> List[Comment]:
    """Get all comments in a post with the specified ID."""
    return db.query(Comment).filter_by(parent_post_id=post_id).order_by(Comment.created.desc()).offset(offset).limit(
        limit).all()


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
    db_comment = db.query(Comment).filter_by(id=comment_id).first()
    db.delete(db_comment)
    db.commit()


def update_comment(db: Session, comment_id: int, **columns: Any) -> Comment:
    """Update the comment with the given ID.

    Enter any `repost.models.Comment` column to update in `**columns`.
    """
    db.query(Comment).filter_by(id=comment_id).update(columns)
    db.commit()

    return get_comment(db, comment_id=comment_id)


def vote_comment(db: Session, *, comment_id: int, author_id: int, vote: int):
    """Update a user's vote on a comment."""
    db_vote = db.query(CommentVote).filter_by(comment_id=comment_id, author_id=author_id).first()
    if db_vote:
        if vote == 0:
            db.delete(db_vote)
        else:
            db_vote.vote = vote
    elif vote != 0:
        db.add(CommentVote(comment_id=comment_id, author_id=author_id, vote=vote))

    db.commit()
    return db.query(Comment).filter_by(id=comment_id).first()
