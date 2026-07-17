from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse
)

from app.crud.comment import (
    create_comment,
    get_comments_by_ticket,
    get_comment_by_id,
    update_comment,
    delete_comment
)

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=CommentResponse
)
def add_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_comment(
        db=db,
        comment=comment,
        user_id=current_user.id
    )


@router.get(
    "/ticket/{ticket_id}",
    response_model=list[CommentResponse]
)
def read_ticket_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_comments_by_ticket(
        db,
        ticket_id
    )


@router.get(
    "/{comment_id}",
    response_model=CommentResponse
)
def read_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(
        db,
        comment_id
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment


@router.put(
    "/{comment_id}",
    response_model=CommentResponse
)
def edit_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = get_comment_by_id(
        db,
        comment_id
    )

    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return update_comment(
        db,
        db_comment,
        comment
    )


@router.delete(
    "/{comment_id}"
)
def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = get_comment_by_id(
        db,
        comment_id
    )

    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    delete_comment(
        db,
        db_comment
    )

    return {
        "message": "Comment deleted successfully"
    }