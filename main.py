#  This is the main file of the app, from here the server starts
# The app and all the controllers are registered here
# You can say that it's the "application.java" file in Spring Boot

from fastapi import FastAPI
from app.controllers.todo_controller import router as todo_router
from app.controllers.entry_controller import router as entry_router
from app.config.database import engine, Base
from app.models.todo_model import Todo
from app.models.entry_model import Entry

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router, prefix="/todos")
app.include_router(entry_router, prefix="/entries")


@app.get("/")
def health():
    return {"message": "the server is running"}