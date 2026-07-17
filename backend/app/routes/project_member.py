from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberResponse
)

from app.crud.project_member import (
    add_member,
    get_project_members,
    get_member,
    delete_member
)

router = APIRouter(
    prefix="/project-members",
    tags=["Project Members"]
)


@router.post(
    "/",
    response_model=ProjectMemberResponse
)
def create_member(
    member: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_member(
        db,
        member
    )


@router.get(
    "/project/{project_id}",
    response_model=list[ProjectMemberResponse]
)
def read_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_project_members(
        db,
        project_id
    )


@router.delete(
    "/{member_id}"
)
def remove_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member = get_member(
        db,
        member_id
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    delete_member(
        db,
        member
    )

    return {
        "message": "Member removed successfully"
    }