# Database configuration file
# This file sets up SQLAlchemy ORM configuration, database engine, and session management

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator

# Database URL (We changed this from todo.db to reflecta.db to force a schema update)
DATABASE_URL = "sqlite:///./reflecta.db"

# Create the engine
# echo=True logs all SQL statements (useful for debugging)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific: allows multiple threads
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
