# This is the User table in the db
# Every user who registers gets a row in this table

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # unique=True means no two users can have the same username
    # Example: ashutosh_11, ASHUTOSH1
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships to data
    entries = relationship("Entry", back_populates="owner")
    todos = relationship("Todo", back_populates="owner")