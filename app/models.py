from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """Base todo model"""
    title: str = Field(..., min_length=1, max_length=200, description="TODO title")
    description: Optional[str] = Field(None, max_length=1000, description="TODO description")
    completed: bool = Field(False, description="Completion status")


class TodoCreate(TodoBase):
    """Model for creating a todo"""
    pass


class TodoUpdate(BaseModel):
    """Model for updating a todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    """Complete todo model with ID"""
    id: int = Field(..., description="TODO ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Learn Kubernetes",
                "description": "Complete Helm labs",
                "completed": False,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }
