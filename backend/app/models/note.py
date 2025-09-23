# Note model - defines the notes table structure

# Import database column types and relationships  
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Import our Base class from database.py
from ..database import Base


class Note(Base):
    """
    Note model - represents a LaTeX note in our system.
    Each note belongs to exactly one user.
    
    This creates a 'notes' table in the database with columns:
    - id: unique identifier for each note
    - user_id: which user owns this note (foreign key to users.id)
    - title: note title for organization
    - latex_content: the actual LaTeX code
    - pdf_url: location of compiled PDF (nullable)
    - status: compilation status (pending, completed, failed)
    - created_at: when note was created
    - updated_at: when note was last modified
    """
    __tablename__ = "notes"
    
    # Primary Key - unique identifier for each note
    id = Column(Integer, primary_key=True, index=True)
    # Same as User model - auto-incrementing unique ID
    
    # Foreign Key - links this note to a specific user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # CRITICAL: This creates the actual database column that stores the link
    # ForeignKey("users.id") means: "this must be a valid ID from users table"
    # nullable=False means: "every note MUST belong to a user"
    # Database will reject: INSERT note WHERE user_id doesn't exist in users table
    
    # Title - short description for organization
    title = Column(String(200), nullable=False)
    # String(200) = max 200 characters (good for titles)
    # nullable=False = every note must have a title
    # Used for: note lists, organization, search
    
    # LaTeX Content - the actual LaTeX code
    latex_content = Column(Text, nullable=False)
    # Text = can store very large content (entire LaTeX documents)
    # nullable=False = every note must have content
    # This is where the actual LaTeX code lives
    
    # PDF URL - location of compiled PDF file
    pdf_url = Column(String, nullable=True)
    # nullable=True = can be empty (notes start without PDFs)
    # Gets filled after successful LaTeX compilation
    # Examples: "s3://bucket/notes/123.pdf" or "/files/note123.pdf"
    
    # Status - compilation status tracking
    status = Column(String, default="pending")
    # Possible values: "pending", "compiling", "completed", "failed"
    # default="pending" = new notes start as "pending" 
    # Used to show compilation progress in UI
    
    # Timestamps - track when note was created and last modified
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # created_at: set once when note is created (never changes)
    # updated_at: automatically updated whenever note is modified
    # onupdate=func.now() = database updates this field on every UPDATE
    
    # Relationship - connect this note back to its owner
    user = relationship("User", back_populates="notes")
    # This completes the bidirectional relationship:
    # note.user → User object who owns this note
    # user.notes → [Note1, Note2, Note3...] (from User model)
    # back_populates="notes" links to the User.notes relationship
    
    def __repr__(self):
        """
        String representation for debugging.
        Shows key info about the note when printed.
        """
        return f"<Note(id={self.id}, title='{self.title}', user_id={self.user_id}, status='{self.status}')>"
