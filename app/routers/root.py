"""
Root endpoints router
"""
from fastapi import APIRouter
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Root"])


@router.get("/")
async def root():
    """Root endpoint with API information"""
    logger.info("Root endpoint accessed")
    return {
        "message": f"Welcome to {Config.APP_NAME}",
        "version": Config.APP_VERSION,
        "environment": Config.ENVIRONMENT,
        "docs_url": "/docs" if Config.ENABLE_DOCS else "disabled",
        "endpoints": {
            "todos": "/todos",
            "health": "/health",
            "liveness": "/health/live",
            "readiness": "/health/ready"
        }
    }
