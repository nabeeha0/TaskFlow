from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_users: int

    total_projects: int

    total_tickets: int


    todo_tickets: int

    progress_tickets: int

    completed_tickets: int


    total_comments: int

    total_attachments: int

    total_project_members: int


    class Config:
        from_attributes = True