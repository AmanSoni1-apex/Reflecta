from sqlalchemy.orm import Session
from app.models.entry_model import Entry

class EntryRepository:

    def save(self,db:Session,entry:Entry)->Entry:
        db.add(entry) 
        db.commit()
        db.refresh(entry)
        return entry

    def get_all(self, db: Session) -> list[Entry]:
        return db.query(Entry).all()

    def get_by_id(self, db: Session, entry_id: int) -> Entry:
        return db.query(Entry).filter(Entry.id == entry_id).first()

    def delete(self, db: Session, entry: Entry):
        db.delete(entry)
        db.commit()

    def get_mood_counts(self, db: Session):
        # 1. Get ALL entries (The raw pile)
        all_entries = db.query(Entry).all()
        
        # 2. Count them manually
        counts = {}
        for entry in all_entries:
            mood = entry.sentiment
            if mood in counts:
                counts[mood] += 1
            else:
                counts[mood] = 1
                
        # 3. Return the result
        return list(counts.items())