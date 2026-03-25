from pydantic import BaseModel
from datetime import date

class ReflectionPeriod(BaseModel):
    start_date: date
    end_date: date

class EmotionStats(BaseModel):
    total_entries: int
    emotions_count: dict[str, int]
    dominant_emotion: str | None = None

class WeeklyReflectionResponse(BaseModel):
    period: ReflectionPeriod
    headline: str
    emotional_summary: str
    patterns: list[str]
    suggestions: list[str]
    stats: EmotionStats

class AdminUserResponse(BaseModel):
    id:int
    username:str
    email:str
    
    
    class Config:
        from_attributes=True