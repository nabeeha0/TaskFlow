from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "Medium"
    status: str = "To Do"
    due_date: Optional[datetime] = None
    project_id: int
    assignee_id: Optional[int] = None


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TicketResponse(BaseModel):
    id: int
    ticket_number: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: Optional[datetime]
    project_id: int
    assignee_id: Optional[int]
    reporter_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True