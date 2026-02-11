from sqlalchemy.orm import Session
from app.repositories.entry_repository import EntryRepository
from app.repositories.todo_repository import TodoRespository


class AnalyticsService:
    def __init__(self):
    # We initialize the repos so that we can use them later on 
        self.entry_repo = EntryRepository()
        self.todo_repo = TodoRespository()
        

    def get_dashboard_stats(self,db:Session):
        # 1. Here we are asking for the raw data 
        raw_moods=self.entry_repo.get_mood_counts(db)
        raw_categories=self.todo_repo.get_category_counts(db)

        # We want to turn [('Happy', 5)] into {"Happy": 5}
        mood_stats=dict(raw_moods)
        category_stats=dict(raw_categories)

        # 3. Final Assembly
        return{
            "mood_trends":mood_stats,
            "productivity_balance":category_stats,
            "total_entries": sum(mood_stats.values()),
            "total_todos": sum(category_stats.values())
        }
    