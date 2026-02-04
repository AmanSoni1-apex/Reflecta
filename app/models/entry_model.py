# The "Mud Pit" (Entry Model)
# This table is designed to hold raw, unstructured thoughts.

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class Entry(Base):
    __tablename__ = "entries"

    # The Unique ID (Just like everything else)
    id = Column(Integer, primary_key=True, index=True)

    # The Raw Thought (The "Mud")
    # We use "Text" instead of "String" because Text can hold huge amounts of data.
    raw_content = Column(Text, nullable=False)

    # The Timestamp
    # We need to know WHEN you had this thought to analyze trends later.
    # func.now() makes the database automatically set the time when we save it.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
