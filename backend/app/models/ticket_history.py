from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from app.database.database import Base


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id = Column(Integer, primary_key=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    changed_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    old_status = Column(String(50))

    new_status = Column(String(50))

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )