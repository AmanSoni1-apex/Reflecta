# Database configuration file
# This file sets up SQLAlchemy ORM configuration, database engine, and session management

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# Grab the Supabase URL from Vercel, or use local SQLite for your PC
DATABASE_URL = os.environ.get("postgresql://postgres:amansoni4144@gmail.com@db.uptjxuaqglnjdhbjhume.supabase.co:5432/postgres", "sqlite:///./reflecta.db")

# Only allow check_same_thread for SQLite (Postgres doesn't need it)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create the engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# SessionLocal factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models to inherit from
Base = declarative_base()

# Dependency function to provide database session to endpoints
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
