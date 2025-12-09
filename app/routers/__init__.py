"""
Routers package initialization
"""
from .health import router as health_router
from .todos import router as todos_router
from .root import router as root_router

__all__ = ["health_router", "todos_router", "root_router"]
