from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from app.database.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True)

    filename = Column(String(255))

    filepath = Column(String(500))

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )