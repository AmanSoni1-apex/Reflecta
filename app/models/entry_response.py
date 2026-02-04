from pydantic import BaseModel 
from datetime import datetime

# When the user sends us a thought, we should reply with a receipt so they know we saved it. The "Receipt" usually contains the data we just saved, plus the new ID we generated.

class EntryResponse(BaseModel):
    id: int
    raw_content: str 
    created_at: datetime
    
    # AI insights (v1)
    sentiment: str | None = None
    summary: str | None = None

    class Config:
        from_attributes = True