# Controller layer - HTTP Request/Response Layer
# Here we handle request and response operations
# This file is used to take all the data from the client and send it to the service
# It's something like the "@RestController" in Java/Spring Boot
# We don't write the controller directly into the main.py file instead we make it separately
# and then register it in the main.py file
# The controller says to the service -> "hey this is the request that came from the client, take this, apply the rules, and give me the result" 




from fastapi import APIRouter, Depends, HTTPException  # APIRouter groups routes; Depends for dependency injection
from sqlalchemy.orm import Session
from app.services.todo_service import TodoService
from app.models.todo_request import TodoCreate
from app.models.todo_response import TodoResponse
from app.config.database import get_db

router = APIRouter()
service = TodoService()


@router.post("/", response_model=TodoResponse)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new Todo
    
    Args:
        todo: TodoCreate schema from request body
        db: Database session injected by FastAPI dependency injection
        
    Returns:
        TodoResponse: Created Todo with ID
    """
    return service.create_todo(db, todo)


@router.get("/", response_model=list[TodoResponse])
def get_todo(db: Session = Depends(get_db)):
    """
    Get all Todos
    
    Args:
        db: Database session injected by FastAPI dependency injection
        
    Returns:
        List of all Todos
    """
    return service.get_all_todos(db)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    """
    Get a single Todo by ID
    """
    todo = service.get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Update a Todo by ID
    """
    updated_todo = service.update_todo(db, todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a Todo by ID
    """
    success = service.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


