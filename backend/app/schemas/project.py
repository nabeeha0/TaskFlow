from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    name: str
    key: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    key: str
    description: Optional[str]
    owner_id: int

    class Config:
        from_attributes = True