#  Service layer - Business Logic Layer
# Here we write the core or the main business logic
# It's something like "@Service" in Spring Boot

from sqlalchemy.orm import Session
from app.repositories.todo_repository import TodoRespository
from app.models.todo_model import Todo
from app.models.todo_request import TodoCreate


class TodoService:
    """
    Service layer for Todo business logic
    Handles validation and delegates database operations to the repository
    """

    def __init__(self):
        self.repo = TodoRespository()

    def create_todo(self, db: Session, todo: TodoCreate) -> Todo:
        """
        Create a new Todo with validation
        
        Args:
            db: SQLAlchemy database session
            todo: TodoCreate schema from API request
            
        Returns:
            The created Todo object
            
        Raises:
            ValueError: If title is empty
        """
        if not todo.title.strip():
            raise ValueError("Title can't be empty")
        
        # Create SQLAlchemy model instance from schema
        db_todo = Todo(title=todo.title, description=todo.description)
        return self.repo.save(db, db_todo)
    
    def get_all_todos(self, db: Session) -> list[Todo]:
        """
        Retrieve all Todos from the database
        
        Args:
            db: SQLAlchemy database session
            
        Returns:
            List of all Todo objects
        """
        return self.repo.find_all(db)

    def update_todo(self, db: Session, todo_id: int, todo_data: Todo):
        existing_todo = self.repo.find_by_id(db, todo_id)
        if not existing_todo:
            return None
        # Convert Pydantic model to dict, excluding defaults if needed (but here we want full update)
        return self.repo.update(db, existing_todo, todo_data.dict())

    def delete_todo(self, db: Session, todo_id: int) -> bool:
        existing_todo = self.repo.find_by_id(db, todo_id)
        if not existing_todo:
            return False
        self.repo.delete(db, existing_todo)
        return True

    def get_todo_by_id(self, db: Session, todo_id: int) -> Todo | None:
        """
        Retrieve a single Todo by ID
        """
        return self.repo.find_by_id(db, todo_id)