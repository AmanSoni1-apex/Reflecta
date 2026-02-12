# The todo_request is used and created so that we can accept the polished or one line content form the user for ex :- 
# {
#   "title": "Buy Milk",
#   "description": "Get 2 liters of full cream milk"
# } 

from pydantic import BaseModel


class TodoCreate(BaseModel):
    # Note: Pydantic is a 'Parser', not just a 'Validator'. 
    # If the user sends a number (like 123) for the title, 
    # Pydantic will 'coerce' (convert) it into a string automatically.
    title: str
    description: str | None = None
    completed: bool = False
    # description = attribute / variable , None = default value ( if the user dont provide the value use these default value's)
    # these values are imp as they act as the fallback plan , str= "Type Hint"
