from sqlalchemy.orm import Session
from app.repositories.entry_repository import EntryRepository
from app.models.entry_model import Entry
from app.models.entry_request import EntryCreate

class EntryService:

    def __init__(self):
        self.repo = EntryRepository() 

    def create_entry(self , db:Session,entry_data:EntryCreate)->Entry:
        db_entry=Entry(raw_content=entry_data.raw_content)
        return self.repo.save(db , db_entry)