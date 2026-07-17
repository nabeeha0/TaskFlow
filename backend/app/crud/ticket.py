from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(
    db: Session,
    ticket: TicketCreate,
    reporter_id: int
):
    # Generate the next ticket number
    last_ticket_number = db.query(
        func.max(Ticket.ticket_number)
    ).scalar()

    next_ticket_number = 1 if last_ticket_number is None else last_ticket_number + 1

    db_ticket = Ticket(
        ticket_number=next_ticket_number,
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        due_date=ticket.due_date,
        project_id=ticket.project_id,
        assignee_id=ticket.assignee_id,
        reporter_id=reporter_id
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return db_ticket


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket_by_id(
    db: Session,
    ticket_id: int
):
    return (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )


def update_ticket(
    db: Session,
    db_ticket: Ticket,
    ticket: TicketUpdate
):
    update_data = ticket.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)

    return db_ticket


def delete_ticket(
    db: Session,
    db_ticket: Ticket
):
    db.delete(db_ticket)
    db.commit()