# Models package - exports all database models
#
# This file makes the models directory into a Python package
# and controls what can be imported from app.models

# Import our database models
from .user import User
from .note import Note

# Explicit export list - only these classes can be imported
# When someone does: from app.models import *
# They get exactly these classes and nothing else
__all__ = [
    "User",
    "Note",
]
