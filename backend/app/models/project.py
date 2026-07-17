from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, unique=True)

    key = Column(String(10), nullable=False, unique=True)

    description = Column(Text)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship(
        "User",
        back_populates="projects"
    )

    tickets = relationship(
        "Ticket",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    members = relationship(
        "ProjectMember",
        back_populates="project"
    )