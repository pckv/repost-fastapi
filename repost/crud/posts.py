from typing import Optional, Any, List

from sqlalchemy.orm import Session

from repost.models import Post, PostVote


def get_posts(db: Session, *, parent_resub_id: int, offset: int = 0, limit: int = 100) -> List[Post]:
    """Get all posts in a resub."""
    return db.query(Post).filter_by(parent_resub_id=parent_resub_id).offset(offset).limit(limit).all()


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


def update_post(db: Session, *, post_id: int, **columns: Any) -> Post:
    """Update the post with the given ID.

    Enter any `repost.models.Post` column to update in `**columns`.
    """
    db.query(Post).filter_by(id=post_id).update(columns)
    db.commit()

    return get_post(db, post_id=post_id)


def delete_post(db: Session, *, post_id: int):
    """Delete the post with the given ID."""
    db_post = db.query(Post).filter_by(id=post_id).first()
    db.delete(db_post)
    db.commit()


def vote_post(db: Session, *, post_id: int, author_id: int, vote: int):
    """Update a user's vote on a post."""
    db_vote = db.query(PostVote).filter_by(post_id=post_id, author_id=author_id).first()
    if db_vote:
        if vote == 0:
            db.delete(db_vote)
        else:
            db_vote.vote = vote
    elif vote != 0:
        db.add(PostVote(post_id=post_id, author_id=author_id, vote=vote))

    db.commit()
    return db.query(Post).filter_by(id=post_id).first()
