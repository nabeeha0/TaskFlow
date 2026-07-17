from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True)