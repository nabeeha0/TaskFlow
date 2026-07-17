from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse
)

from app.crud.ticket import (
    create_ticket,
    get_all_tickets,
    get_ticket_by_id,
    update_ticket,
    delete_ticket
)

from app.auth.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/", response_model=TicketResponse)
def create_new_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_ticket(
        db=db,
        ticket=ticket,
        reporter_id=current_user.id
    )


@router.get("/", response_model=list[TicketResponse])
def read_all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_tickets(db)


@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
def edit_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = get_ticket_by_id(db, ticket_id)

    if not db_ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return update_ticket(
        db,
        db_ticket,
        ticket
    )


@router.delete("/{ticket_id}")
def remove_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = get_ticket_by_id(db, ticket_id)

    if not db_ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    delete_ticket(
        db,
        db_ticket
    )

    return {
        "message": "Ticket deleted successfully"
    }