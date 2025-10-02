# User schemas for API request/response validation

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Base user schema with common fields
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a new user (what we receive from API)
class UserCreate(UserBase):
    password: str  # Plain password (will be hashed)

# Schema for user responses (what we send back via API)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models

# Schema for user with their notes included
class UserWithNotes(UserResponse):
    notes: List["NoteResponse"] = []
