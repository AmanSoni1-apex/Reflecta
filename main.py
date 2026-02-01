#  This is the main file of the app, from here the server starts
# The app and all the controllers are registered here
# You can say that it's the "application.java" file in Spring Boot

from fastapi import FastAPI
from app.controllers.todo_controller import router
from app.config.database import engine, Base
from app.models.todo_model import Todo

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/todos")


@app.get("/")
def health():
    return {"message": "the server is running"}