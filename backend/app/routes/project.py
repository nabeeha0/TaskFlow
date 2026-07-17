from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)

from app.crud.project import (
    create_project,
    get_projects,
    get_project_by_id,
    update_project,
    delete_project
)

from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "/",
    response_model=ProjectResponse
)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_project(
        db=db,
        project=project,
        owner_id=current_user.id
    )


@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def read_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_projects(db)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(
        db,
        project_id
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def edit_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = get_project_by_id(
        db,
        project_id
    )

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return update_project(
        db,
        db_project,
        project
    )


@router.delete(
    "/{project_id}"
)
def remove_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = get_project_by_id(
        db,
        project_id
    )

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    delete_project(
        db,
        db_project
    )

    return {
        "message": "Project deleted successfully"
    }