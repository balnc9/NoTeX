# Database initialization script
# This creates all tables defined in our models

from app.database import engine, Base
from app.models import User, Note  # Import models to register them

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
