from sqlalchemy.orm import Session

from app.models.label import Label
from app.schemas.label import LabelCreate, LabelUpdate


def create_label(
    db: Session,
    label: LabelCreate
):
    db_label = Label(
        name=label.name
    )

    db.add(db_label)
    db.commit()
    db.refresh(db_label)

    return db_label


def get_labels(db: Session):
    return db.query(Label).all()


def get_label_by_id(
    db: Session,
    label_id: int
):
    return (
        db.query(Label)
        .filter(Label.id == label_id)
        .first()
    )


def update_label(
    db: Session,
    db_label: Label,
    label: LabelUpdate
):
    db_label.name = label.name

    db.commit()
    db.refresh(db_label)

    return db_label


def delete_label(
    db: Session,
    db_label: Label
):
    db.delete(db_label)
    db.commit()