from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.label import (
    LabelCreate,
    LabelUpdate,
    LabelResponse
)

from app.crud.label import (
    create_label,
    get_labels,
    get_label_by_id,
    update_label,
    delete_label
)

router = APIRouter(
    prefix="/labels",
    tags=["Labels"]
)


@router.post(
    "/",
    response_model=LabelResponse
)
def create_new_label(
    label: LabelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_label(db, label)


@router.get(
    "/",
    response_model=list[LabelResponse]
)
def read_labels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_labels(db)


@router.get(
    "/{label_id}",
    response_model=LabelResponse
)
def read_label(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    label = get_label_by_id(db, label_id)

    if not label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    return label


@router.put(
    "/{label_id}",
    response_model=LabelResponse
)
def edit_label(
    label_id: int,
    label: LabelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_label = get_label_by_id(db, label_id)

    if not db_label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    return update_label(
        db,
        db_label,
        label
    )


@router.delete(
    "/{label_id}"
)
def remove_label(
    label_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_label = get_label_by_id(db, label_id)

    if not db_label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    delete_label(
        db,
        db_label
    )

    return {
        "message": "Label deleted successfully"
    }