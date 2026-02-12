#  This is the main file of the app, from here the server starts
# The app and all the controllers are registered here
# You can say that it's the "application.java" file in Spring Boot

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.controllers.todo_controller import router as todo_router
from app.controllers.entry_controller import router as entry_router
from app.config.database import engine, Base
from app.models.todo_model import Todo
from app.models.entry_model import Entry
from app.controllers.analytics_controller import router as analytics_router
import os

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Ensure 'static' directory exists for serving
if not os.path.exists("static"):
    os.makedirs("static")

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    # Serve the professional UI as the home page
    return FileResponse('static/index.html')

# Register API Routers
app.include_router(todo_router, prefix="/todos")
app.include_router(entry_router, prefix="/entries")
app.include_router(analytics_router, prefix="/analytics")