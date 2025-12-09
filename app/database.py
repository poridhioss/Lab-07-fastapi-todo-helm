from typing import List
from datetime import datetime
from models import Todo, TodoCreate


# In-memory storage
todos_db: List[Todo] = []
next_id = 1


def create_todo(todo: TodoCreate) -> Todo:
    """Create a new TODO item"""
    global next_id
    new_todo = Todo(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    todos_db.append(new_todo)
    next_id += 1
    return new_todo


def get_all_todos(skip: int = 0, limit: int = 100) -> List[Todo]:
    """Get all TODO items with pagination"""
    return todos_db[skip : skip + limit]


def get_todo_by_id(todo_id: int) -> Todo | None:
    """Get a specific TODO by ID"""
    return next((t for t in todos_db if t.id == todo_id), None)


def delete_todo(todo: Todo) -> None:
    """Delete a TODO item"""
    todos_db.remove(todo)


def get_todo_count() -> int:
    """Get total number of TODO items"""
    return len(todos_db)


def get_completed_count() -> int:
    """Get number of completed TODO items"""
    return sum(1 for t in todos_db if t.completed)
