#  Service layer - Business Logic Layer
# Here we write the core or the main business logic
# It's something like "@Service" in Spring Boot

from sqlalchemy.orm import Session
from app.repositories.todo_repository import TodoRespository
from app.models.todo_model import Todo
from app.models.todo_request import TodoCreate

import ollama
import json
import re 


class TodoService:
    """
    Service layer for Todo business logic
    Handles validation and delegates database operations to the repository
    """

    def __init__(self):
        self.repo = TodoRespository()

    def create_todo(self, db: Session, todo: TodoCreate, background_tasks=None) -> Todo:
        if not todo.title.strip():
            raise ValueError("Title can't be empty")
        
        # 1. Immediate Save with defaults
        db_todo = Todo(
            title=todo.title, 
            description=todo.description,
            priority="Medium",
            category="General",
            completed=False
        )
        saved_todo = self.repo.save(db, db_todo)

        # 2. Queue AI Refinement in the background (Non-blocking)
        if background_tasks:
            background_tasks.add_task(self.background_refine, saved_todo.id)
            
        return saved_todo

    def background_refine(self, todo_id: int):
        """Runs in the background to update the task with AI insights."""
        from app.config.database import SessionLocal
        db = SessionLocal()
        try:
            todo = self.repo.find_by_id(db, todo_id)
            if not todo: return
            
            refinement = self.refine_todo(todo.title, todo.description or "")
            self.repo.update(db, todo, {
                "priority": refinement.get("priority", "Medium"),
                "category": refinement.get("category", "General")
            })
        finally:
            db.close()

    
    def get_all_todos(self, db: Session) -> list[Todo]:
        return self.repo.find_all(db)

    def update_todo(self, db: Session, todo_id: int, todo_data: TodoCreate):
        existing_todo = self.repo.find_by_id(db, todo_id)
        if not existing_todo:
            return None
        return self.repo.update(db, existing_todo, todo_data.model_dump(exclude_unset=True))


    def delete_todo(self, db: Session, todo_id: int) -> bool:
        existing_todo = self.repo.find_by_id(db, todo_id)
        if not existing_todo:
            return False
        self.repo.delete(db, existing_todo)
        return True

    def delete_todos(self, db: Session, ids: list[int]) -> int:
        """
        Deletes multiple todos and returns the count of deleted items.
        """
        count = 0
        for todo_id in ids:
            if self.delete_todo(db, todo_id):
                count += 1
        return count

    def get_todo_by_id(self, db: Session, todo_id: int) -> Todo | None:

        return self.repo.find_by_id(db, todo_id)

    def refine_todo(self, title: str, description: str = ""):
        # The AI "Refiner" Prompt
        system_prompt = """
        You are a productivity expert for the 'Reflecta' app.
        Analyze the task and return ONLY a JSON object with:
        "category": (One word: Work, Personal, Home, Health, Errand, or Other)
        "priority": (One word: High, Medium, or Low)
        """
        
        content = f"Task: {title}\nDescription: {description}"
        
        try:
            response = ollama.chat(model='gemma3:4b', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': content},
            ])
            ai_text = response['message']['content']
            
            # Simple JSON extraction
            json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print(f"AI Refinement failed: {e}")
            
        return {"category": "General", "priority": "Medium"}