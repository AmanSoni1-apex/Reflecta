# The "Mud Pit" (Entry Model)
# This table is designed to hold raw, unstructured thoughts.

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.config.database import Base
from sqlalchemy.orm import relationship

class Entry(Base):
    __tablename__ = "entries"

    # The Unique ID (Just like everything else)
    id = Column(Integer, primary_key=True, index=True)

    # The Raw Thought (The "Mud")
    raw_content = Column(Text, nullable=False)

    # AI Insights (The "Refinement")
    # We save these so they appear in your history (GET /entries)
    sentiment = Column(String(50), nullable=True)
    summary = Column(Text, nullable=True)

    # User Link
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="entries")

    # The Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
