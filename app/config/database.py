# Database configuration file

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator
import os

# 🔥 Get DATABASE_URL (NO fallback to SQLite in production)
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL not set in environment")

# Create engine (PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # important for production
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base model
Base = declarative_base()

# Dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()