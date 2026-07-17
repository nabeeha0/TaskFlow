from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


def create_comment(
    db: Session,
    comment: CommentCreate,
    user_id: int
):
    db_comment = Comment(
        content=comment.content,
        ticket_id=comment.ticket_id,
        user_id=user_id
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def get_comments_by_ticket(
    db: Session,
    ticket_id: int
):
    return (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .all()
    )


def get_comment_by_id(
    db: Session,
    comment_id: int
):
    return (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )


def update_comment(
    db: Session,
    db_comment: Comment,
    comment: CommentUpdate
):
    db_comment.content = comment.content

    db.commit()
    db.refresh(db_comment)

    return db_comment


def delete_comment(
    db: Session,
    db_comment: Comment
):
    db.delete(db_comment)
    db.commit()