# The entry request file is created and used so that so that we can accept the raw content from the user. 
# Example Input:-
# {
#   "raw_content": "I felt really stressed today because the meeting went long and I missed my lunch..."
# } 
from pydantic import BaseModel, field_validator  
class EntryCreate(BaseModel):
    raw_content : str

    @field_validator('raw_content')
    def not_empty(cls, v):   #not_empty(ModelClass, value) here the modelClass -> EntryCreate and v-> the value we are validating , this is not the normal function this is a validator function of the pydantic   
        if not v.strip():
            raise ValueError('Content cannot be empty or whitespace only')
        return v