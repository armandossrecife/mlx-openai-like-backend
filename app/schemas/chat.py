from pydantic import BaseModel
from datetime import datetime

class ChatSessionCreate(BaseModel):
    title: str | None = None

class ChatSessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime

class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime