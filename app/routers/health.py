"""
Health check endpoints router
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging

from ..database import get_todo_count

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness probe endpoint
    Returns 200 if the application is alive
    Kubernetes will restart the container if this fails
    """
    logger.debug("Liveness check called")
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Readiness probe endpoint
    Returns 200 if the application is ready to serve traffic
    Kubernetes will stop sending traffic if this fails
    """
    logger.debug("Readiness check called")
    
    # Check if application is ready
    # In a real app, you'd check database connections, etc.
    is_ready = True
    
    if not is_ready:
        logger.warning("Application is not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready"
        )
    
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "todo_count": get_todo_count()
    }


@router.get("", status_code=status.HTTP_200_OK)
async def health_check():
    """
    General health check endpoint
    Returns application status and configuration
    """
    from ..config import Config
    
    logger.debug("Health check called")
    return {
        "status": "healthy",
        "app_name": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "environment": Config.ENVIRONMENT,
        "todo_count": get_todo_count(),
        "max_items": Config.MAX_ITEMS,
        "timestamp": datetime.utcnow().isoformat()
    }
