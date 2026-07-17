from pydantic import BaseModel


class AttachmentCreate(BaseModel):
    filename: str
    filepath: str
    ticket_id: int


class AttachmentUpdate(BaseModel):
    filename: str
    filepath: str


class AttachmentResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    ticket_id: int

    class Config:
        from_attributes = True