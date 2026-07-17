from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.attachment import (
    AttachmentCreate,
    AttachmentUpdate,
    AttachmentResponse
)

from app.crud.attachment import (
    create_attachment,
    get_attachments,
    get_attachment_by_id,
    update_attachment,
    delete_attachment
)

router = APIRouter(
    prefix="/attachments",
    tags=["Attachments"]
)


@router.post(
    "/",
    response_model=AttachmentResponse
)
def create_new_attachment(
    attachment: AttachmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_attachment(
        db,
        attachment
    )


@router.get(
    "/",
    response_model=list[AttachmentResponse]
)
def read_attachments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_attachments(db)


@router.get(
    "/{attachment_id}",
    response_model=AttachmentResponse
)
def read_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attachment = get_attachment_by_id(
        db,
        attachment_id
    )

    if not attachment:
        raise HTTPException(
            status_code=404,
            detail="Attachment not found"
        )

    return attachment


@router.put(
    "/{attachment_id}",
    response_model=AttachmentResponse
)
def edit_attachment(
    attachment_id: int,
    attachment: AttachmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_attachment = get_attachment_by_id(
        db,
        attachment_id
    )

    if not db_attachment:
        raise HTTPException(
            status_code=404,
            detail="Attachment not found"
        )

    return update_attachment(
        db,
        db_attachment,
        attachment
    )


@router.delete(
    "/{attachment_id}"
)
def remove_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_attachment = get_attachment_by_id(
        db,
        attachment_id
    )

    if not db_attachment:
        raise HTTPException(
            status_code=404,
            detail="Attachment not found"
        )

    delete_attachment(
        db,
        db_attachment
    )

    return {
        "message": "Attachment deleted successfully"
    }