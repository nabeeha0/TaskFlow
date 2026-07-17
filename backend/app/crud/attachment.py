from sqlalchemy.orm import Session

from app.models.attachment import Attachment
from app.schemas.attachment import (
    AttachmentCreate,
    AttachmentUpdate
)


def create_attachment(
    db: Session,
    attachment: AttachmentCreate
):
    db_attachment = Attachment(
        filename=attachment.filename,
        filepath=attachment.filepath,
        ticket_id=attachment.ticket_id
    )

    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)

    return db_attachment


def get_attachments(db: Session):
    return db.query(Attachment).all()


def get_attachment_by_id(
    db: Session,
    attachment_id: int
):
    return (
        db.query(Attachment)
        .filter(Attachment.id == attachment_id)
        .first()
    )


def update_attachment(
    db: Session,
    db_attachment: Attachment,
    attachment: AttachmentUpdate
):
    db_attachment.filename = attachment.filename
    db_attachment.filepath = attachment.filepath

    db.commit()
    db.refresh(db_attachment)

    return db_attachment


def delete_attachment(
    db: Session,
    db_attachment: Attachment
):
    db.delete(db_attachment)
    db.commit()