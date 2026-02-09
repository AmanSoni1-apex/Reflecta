from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.entry_service import EntryService
from app.models.entry_request import EntryCreate
from app.models.entry_response import EntryResponse

router=APIRouter()
service=EntryService()

@router.post("/",response_model=EntryResponse)
def create_entry(entry :EntryCreate , db: Session=Depends(get_db)):
    return service.create_entry(db , entry)

@router.get("/", response_model=list[EntryResponse])
def get_entries(db: Session = Depends(get_db)):
    return service.get_all_entries(db)