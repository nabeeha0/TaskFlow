from pydantic import BaseModel


class ProjectMemberCreate(BaseModel):
    project_id: int
    user_id: int
    role: str


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str

    class Config:
        from_attributes = True