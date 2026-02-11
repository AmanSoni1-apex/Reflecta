from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.services.analytics_service import AnalyticsService
from app.config.database import get_db

#  Here we initializing the Router and the service's 
router=APIRouter()
service=AnalyticsService()


#  Define the GET endpoint 
@router.get("/dashboard")
def get_dashboard(db:Session=Depends(get_db)):
    """
    Get the introspection dashboard (Mood trends + productivity balance)
    """
    return service.get_dashboard_stats(db)

