# SQLAlchemy ORM model for the Todo database table

from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255) , nullable=False)
    description = Column(String(1024), nullable=True)



  