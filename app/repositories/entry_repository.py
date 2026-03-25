from sqlalchemy.orm import Session
from app.models.entry_model import Entry

class EntryRepository:

    def save(self,db:Session,entry:Entry)->Entry:
        db.add(entry) 
        db.commit()
        db.refresh(entry)
        return entry

    def get_all(self, db: Session, user_id: int) -> list[Entry]:
        return db.query(Entry).filter(Entry.user_id == user_id).all()

    def get_by_id(self, db: Session, entry_id: int, user_id: int) -> Entry:
        return db.query(Entry).filter(Entry.id == entry_id, Entry.user_id == user_id).first()

    def delete(self, db: Session, entry: Entry):
        db.delete(entry)
        db.commit()

    def get_mood_counts(self, db: Session, user_id: int):
        # 1. Get ONLY user's entries
        all_entries = db.query(Entry).filter(Entry.user_id == user_id).all()
        
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