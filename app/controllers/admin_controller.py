from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.auth.deps import get_current_admin_user
from app.auth.auth_models import User
from app.models.weekly_reflection_response import AdminUserResponse

router = APIRouter()

@router.get("/users", response_model=list[AdminUserResponse])
def list_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin_user)):
    # .all() returns a list of User objects which matches the response_model
    return db.query(User).all()
