from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    ticket_number = Column(Integer, nullable=False)

    title = Column(String(255), nullable=False)

    description = Column(Text)

    status = Column(String(50), default="To Do")

    priority = Column(String(50), default="Medium")

    due_date = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    assignee_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    reporter_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    project = relationship(
        "Project",
        back_populates="tickets"
    )

    assignee = relationship(
        "User",
        foreign_keys=[assignee_id]
    )

    reporter = relationship(
        "User",
        foreign_keys=[reporter_id]
    )

    comments = relationship(
        "Comment",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )