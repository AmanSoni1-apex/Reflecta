from sqlalchemy.orm import Session
from app.repositories.entry_repository import EntryRepository
from app.repositories.todo_repository import TodoRespository


class AnalyticsService:
    def __init__(self):
    # We initialize the repos so that we can use them later on 
        self.entry_repo = EntryRepository()
        self.todo_repo = TodoRespository()
        

    def get_dashboard_stats(self, db: Session):
        """
        Calculates advanced metrics for the Zenith Obsidian dashboard.
        Includes distribution, WoW sentiment velocity, and daily activity heatmaps.
        """
        from datetime import datetime, timedelta
        
        all_entries = self.entry_repo.get_all(db)
        all_todos = self.todo_repo.find_all(db)

        # 1. Distribution & Volume
        mood_dist = {}
        for e in all_entries:
            m = e.sentiment or 'Neutral'
            mood_dist[m] = mood_dist.get(m, 0) + 1
        
        category_dist = {}
        for t in all_todos:
            c = t.category or 'General'
            category_dist[c] = category_dist.get(c, 0) + 1

        # 2. Sentiment Velocity (Week-over-Week trend of positive signals)
        now = datetime.now()
        this_week_start = now - timedelta(days=7)
        prev_week_start = now - timedelta(days=14)

        pos_signals = ['Happy', 'Focused', 'Calm', 'Proud', 'Excited']
        
        this_week_pos = sum(1 for e in all_entries if e.created_at and e.created_at.replace(tzinfo=None) >= this_week_start and e.sentiment in pos_signals)
        prev_week_pos = sum(1 for e in all_entries if e.created_at and e.created_at.replace(tzinfo=None) >= prev_week_start and e.created_at.replace(tzinfo=None) < this_week_start and e.sentiment in pos_signals)

        velocity = 0
        if prev_week_pos > 0:
            velocity = ((this_week_pos - prev_week_pos) / prev_week_pos) * 100
        elif this_week_pos > 0:
            velocity = 100.0

        # 3. Activity Grid (Daily entry volume for Heatmap)
        activity_grid = {}
        # Pre-fill last 30 days with 0
        for i in range(30):
            d = (now - timedelta(days=i)).strftime('%Y-%m-%d')
            activity_grid[d] = 0
            
        for e in all_entries:
            if e.created_at:
                d_str = e.created_at.strftime('%Y-%m-%d')
                if d_str in activity_grid:
                    activity_grid[d_str] += 1

        return {
            "mood_distribution": mood_dist,
            "category_distribution": category_dist,
            "total_entries": len(all_entries),
            "total_todos": len(all_todos),
            "sentiment_velocity": round(velocity, 1),
            "activity_heatmap": activity_grid
        }

    