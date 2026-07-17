from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.project import Project
from app.models.ticket import Ticket
from app.models.comment import Comment
from app.models.attachment import Attachment
from app.models.project_member import ProjectMember


def get_dashboard_data(db: Session):

    total_tickets = db.query(
        func.count(Ticket.id)
    ).scalar()


    todo_tickets = db.query(
        func.count(Ticket.id)
    ).filter(
        Ticket.status == "To Do"
    ).scalar()


    progress_tickets = db.query(
        func.count(Ticket.id)
    ).filter(
        Ticket.status == "In Progress"
    ).scalar()


    completed_tickets = db.query(
        func.count(Ticket.id)
    ).filter(
        Ticket.status == "Done"
    ).scalar()


    return {

        "total_users": db.query(
            func.count(User.id)
        ).scalar(),


        "total_projects": db.query(
            func.count(Project.id)
        ).scalar(),


        "total_tickets": total_tickets,


        "todo_tickets": todo_tickets,


        "progress_tickets": progress_tickets,


        "completed_tickets": completed_tickets,


        "total_comments": db.query(
            func.count(Comment.id)
        ).scalar(),


        "total_attachments": db.query(
            func.count(Attachment.id)
        ).scalar(),


        "total_project_members": db.query(
            func.count(ProjectMember.id)
        ).scalar()
    }