# Pydantic schema for Todo creation requests
# This schema defines what data the API receives when creating a new Todo

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    # description = attribute / variable , None = default value ( if the user dont provide the value use these default value's)
    # these values are imp as they act as the fallback plan , str= "Type Hint"
