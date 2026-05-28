"""
Database configuration and connection setup
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://erp_admin:password@localhost:5432/erp_db"
)

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DATABASE_ECHO", "False").lower() == "true",
    poolclass=NullPool
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base for models
Base = declarative_base()

# Dependency function for FastAPI
def get_db():
    """
    Dependency for getting database session in FastAPI routes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()