from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    username = Column(String(50), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner")

    memberships = relationship("ProjectMember", back_populates="user")

    assigned_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.assignee_id"
    )

    reported_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.reporter_id"
    )