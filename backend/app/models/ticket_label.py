from sqlalchemy import Column, Integer, ForeignKey

from app.database.database import Base


class TicketLabel(Base):
    __tablename__ = "ticket_labels"

    id = Column(Integer, primary_key=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    label_id = Column(
        Integer,
        ForeignKey("labels.id")
    )