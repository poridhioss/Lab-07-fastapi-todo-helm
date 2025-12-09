"""
TODO items endpoints router
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Todo, TodoCreate, TodoUpdate
from config import Config
import database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/todos", tags=["TODOs"])


@router.get("", response_model=List[Todo])
async def get_todos(skip: int = 0, limit: int = 100):
    """
    Get all TODO items
    - **skip**: Number of items to skip (pagination)
    - **limit**: Maximum number of items to return
    """
    logger.info(f"Getting TODOs (skip={skip}, limit={limit})")
    todos = database.get_all_todos(skip, limit)
    logger.info(f"Returning {len(todos)} TODOs")
    return todos


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Get a specific TODO by ID"""
    logger.info(f"Getting TODO with id={todo_id}")
    
    todo = database.get_todo_by_id(todo_id)
    if not todo:
        logger.warning(f"TODO with id={todo_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with id {todo_id} not found"
        )
    
    logger.info(f"Found TODO: {todo.title}")
    return todo


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo_endpoint(todo: TodoCreate):
    """Create a new TODO item"""
    logger.info(f"Creating new TODO: {todo.title}")
    
    # Check max items limit
    if database.get_todo_count() >= Config.MAX_ITEMS:
        logger.error(f"Maximum TODO items limit reached ({Config.MAX_ITEMS})")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum number of TODOs ({Config.MAX_ITEMS}) reached"
        )
    
    new_todo = database.create_todo(todo)
    logger.info(f"Created TODO with id={new_todo.id}")
    return new_todo


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update an existing TODO item"""
    logger.info(f"Updating TODO with id={todo_id}")
    
    todo = database.get_todo_by_id(todo_id)
    if not todo:
        logger.warning(f"TODO with id={todo_id} not found for update")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with id {todo_id} not found"
        )
    
    # Update fields if provided
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    
    todo.updated_at = datetime.utcnow()
    
    logger.info(f"Updated TODO: {todo.title}")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_endpoint(todo_id: int):
    """Delete a TODO item"""
    logger.info(f"Deleting TODO with id={todo_id}")
    
    todo = database.get_todo_by_id(todo_id)
    if not todo:
        logger.warning(f"TODO with id={todo_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with id {todo_id} not found"
        )
    
    database.delete_todo(todo)
    logger.info(f"Deleted TODO: {todo.title}")
    return None


@router.get("/stats/summary", tags=["Statistics"])
async def get_stats():
    """Get TODO statistics"""
    logger.info("Getting TODO statistics")
    
    total = database.get_todo_count()
    completed = database.get_completed_count()
    pending = total - completed
    
    stats = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": (completed / total * 100) if total > 0 else 0
    }
    
    logger.info(f"Stats: {stats}")
    return stats
