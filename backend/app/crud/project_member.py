from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember
from app.schemas.project_member import ProjectMemberCreate


def add_member(
    db: Session,
    member: ProjectMemberCreate
):
    db_member = ProjectMember(
        project_id=member.project_id,
        user_id=member.user_id,
        role=member.role
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member


def get_project_members(
    db: Session,
    project_id: int
):
    return (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )


def get_member(
    db: Session,
    member_id: int
):
    return (
        db.query(ProjectMember)
        .filter(ProjectMember.id == member_id)
        .first()
    )


def delete_member(
    db: Session,
    db_member: ProjectMember
):
    db.delete(db_member)
    db.commit()