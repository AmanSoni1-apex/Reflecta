# Pydantic schema for Todo API responses
# This schema defines what data the API sends back to clients

from pydantic import BaseModel


class TodoResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    description: str | None
    priority:str | None = None
    category:str | None = None