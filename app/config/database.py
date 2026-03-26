# Database configuration file
# This file sets up SQLAlchemy ORM configuration, database engine, and session management

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# Use /tmp for read-write access in serverless environments like Vercel
if os.environ.get("VERCEL")=="1":
    DATABASE_URL =  "sqlite:////tmp/reflecta.db"
else:
    DATABASE_URL = "sqlite:///./reflecta.db"

# For SQLite, we need connect_args={"check_same_thread": False}
connect_args = {"check_same_thread": False}

# Create the engine
# echo=True logs all SQL statements (useful for debugging)
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
