from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.services.analytics_service import AnalyticsService
from app.config.database import get_db
from app.auth.deps import get_current_user
from app.auth.auth_models import User
from app.models.weekly_reflection_response import WeeklyReflectionResponse

#  Here we initializing the Router and the service's 
router=APIRouter()
service=AnalyticsService()


#  Define the GET endpoint 
@router.get("/dashboard")
def get_dashboard(db:Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get the introspection dashboard (Mood trends + productivity balance)
    """
    return service.get_dashboard_stats(db, current_user.id)


@router.get("/weekly-reflection", response_model=WeeklyReflectionResponse)
def get_weekly_reflection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_weekly_reflection(db, current_user.id)