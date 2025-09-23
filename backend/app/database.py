# The database connection setup - this file handles all database communication

# Import the core SQLAlchemy components
from sqlalchemy import create_engine          # Creates the database connection
from sqlalchemy.ext.declarative import declarative_base   # Base class for our table models  
from sqlalchemy.orm import sessionmaker      # Factory to create database sessions

# Database URL - tells SQLAlchemy where to store data
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"
# Breaking this down:
# sqlite://    = Use SQLite database engine
# ./           = Current directory (backend/)  
# notes.db     = File name for our database

# Create the database engine - this manages the actual connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific setting
)
# What this does:
# 1. Creates connection to notes.db (creates file if doesn't exist)
# 2. check_same_thread=False allows multiple threads (needed for web servers)
# 3. This engine will be reused for all database operations

# Create session factory - this creates new sessions for each request
SessionLocal = sessionmaker(
    autocommit=False,    # Don't auto-save changes (we'll control when)
    autoflush=False,     # Don't auto-send SQL until we're ready
    bind=engine          # Connect this session factory to our engine
)
# What this creates:
# SessionLocal() -> creates a new session
# Each session is like a "shopping cart" for database operations
# Multiple users can have separate sessions simultaneously

# Create the base class for all our database models  
Base = declarative_base()
# What this does:
# 1. Every table class (User, Note) will inherit from Base
# 2. Base provides common functionality like __repr__, __tablename__, etc.
# 3. Base.metadata contains info about all tables (used for creating/dropping)
# 
# Usage: class User(Base): ...
#        class Note(Base): ...

# Helper function to get a database session
def get_db():
    """
    Creates a new database session for each request.
    This will be used as a FastAPI dependency.
    
    Usage in FastAPI:
    @app.post("/notes")
    def create_note(db: Session = Depends(get_db)):
        # db is a fresh session for this request
    """
    db = SessionLocal()  # Create new session
    try:
        yield db         # Give session to the request
    finally:
        db.close()       # Always close session when done
