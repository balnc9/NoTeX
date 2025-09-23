# User model - defines the users table structure

# Import database column types and relationships
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Import our Base class from database.py
from ..database import Base


class User(Base):
    """
    User model - represents a user account in our system.
    Each user can have multiple LaTeX notes.
    
    This creates a 'users' table in the database with columns:
    - id: unique identifier for each user
    - email: user's email address (must be unique)
    - hashed_password: securely stored password
    - created_at: when the account was created
    """
    __tablename__ = "users"  # This becomes the SQL table name
    
    # Primary Key - unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)
    # What this does:
    # - Integer: stores numbers (1, 2, 3, 4...)
    # - primary_key=True: makes this the unique identifier
    # - index=True: creates database index for fast lookups
    # SQLite auto-increments this: first user gets 1, second gets 2, etc.
    
    # Email - user's login credential  
    email = Column(String, unique=True, index=True)
    # What this does:
    # - String: stores text (up to default length limit)
    # - unique=True: prevents duplicate email addresses
    # - index=True: fast lookups when user logs in
    # Database will reject: INSERT user WHERE email already exists
    
    # Password - NEVER store plaintext passwords!
    hashed_password = Column(String)
    # SECURITY: We store bcrypt hash, not actual password
    # User types: "mypassword123"
    # We store: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj"
    # Even if database is stolen, hackers can't get real passwords
    # bcrypt is slow by design - makes brute force attacks impractical
    
    # Timestamp - when was this user account created?
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # What this does:
    # - DateTime(timezone=True): stores date + time + timezone info
    # - server_default=func.now(): database automatically sets current time
    # - User doesn't need to specify this - happens automatically
    # - Useful for: account age, analytics, debugging, audit logs
    
    # Relationship - connect this user to their notes
    notes = relationship("Note", back_populates="user")
    # What this creates:
    # user.notes → [Note1, Note2, Note3...] (list of user's notes)
    # This is NOT a database column - it's a Python property
    # SQLAlchemy automatically queries notes table when you access user.notes
    # "Note" refers to the Note model class (we'll create this next)
    
    def __repr__(self):
        """
        String representation for debugging.
        When you print(user), you'll see something useful instead of memory address.
        """
        return f"<User(id={self.id}, email={self.email})>"
