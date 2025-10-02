# Schemas package - exports all Pydantic schemas

from .user import UserBase, UserCreate, UserResponse, UserWithNotes
from .note import NoteBase, NoteCreate, NoteUpdate, NoteResponse, NoteWithUser

# Fix forward references for circular imports
UserWithNotes.model_rebuild()
NoteWithUser.model_rebuild()

__all__ = [
    "UserBase", "UserCreate", "UserResponse", "UserWithNotes",
    "NoteBase", "NoteCreate", "NoteUpdate", "NoteResponse", "NoteWithUser",
]
