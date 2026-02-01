# Repository layer - Data Access Layer
# This layer handles all database operations
# Uses SQLAlchemy ORM to interact with the database instead of in-memory list

from sqlalchemy.orm import Session
from app.models.todo_model import Todo


class TodoRespository:
    """
    Repository for managing Todo database operations
    Provides methods to save and retrieve Todos from the database
    """

    def save(self, db: Session, todo: Todo) -> Todo:
        """
        Save a new Todo to the database
        
        Args:
            db: SQLAlchemy database session
            todo: Todo object to save
            
        Returns:
            The saved Todo object with generated ID
        """
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def find_all(self, db: Session) -> list[Todo]:
        """
        Retrieve all Todos from the database
        
        Args:
            db: SQLAlchemy database session
            
        Returns:
            List of all Todo objects
        """
        return db.query(Todo).all()

    def find_by_id(self, db: Session, todo_id: int) -> Todo | None:
        """
        Retrieve a single Todo by its ID
        """
        return db.query(Todo).filter(Todo.id == todo_id).first()

