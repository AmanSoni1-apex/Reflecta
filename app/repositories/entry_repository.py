from sqlalchemy.orm import Session
from app.models.entry_model import Entry

class EntryRepository:

    def save(self,db:Session,entry:Entry)->Entry:
        db.add(entry) 
        db.commit()
        db.refresh(entry)
        return entry