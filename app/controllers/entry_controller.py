from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.auth.deps import get_current_user
from app.auth.auth_models import User
from app.services.entry_service import EntryService
from app.models.entry_request import EntryCreate
from app.models.entry_response import EntryResponse

router=APIRouter()
service=EntryService()

@router.post("/",response_model=EntryResponse)
def create_entry(entry :EntryCreate , db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.create_entry(db, entry, current_user.id)

@router.get("/", response_model=list[EntryResponse])
def get_entries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_all_entries(db, current_user.id)

@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = service.delete_entry(db, entry_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry deleted successfully"}