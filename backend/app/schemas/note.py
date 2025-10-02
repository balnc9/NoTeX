# Note schemas for API request/response validation

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base note schema with common fields
class NoteBase(BaseModel):
    title: str
    latex_content: str

# Schema for creating a new note (what we receive from API)
class NoteCreate(NoteBase):
    pass  # Same as base for now

# Schema for updating a note
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    latex_content: Optional[str] = None

# Schema for note responses (what we send back via API)
class NoteResponse(NoteBase):
    id: int
    user_id: int
    pdf_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schema for note with user information included
class NoteWithUser(NoteResponse):
    user: "UserResponse"
