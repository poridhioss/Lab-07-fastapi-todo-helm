from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
import os
import sys

from config import Config
from models import TodoCreate
import database
from routers import health_router, todos_router, root_router

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Get log level from environment variable (default: INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout for Kubernetes
    ]
)

logger = logging.getLogger(__name__)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

# Create FastAPI app
app = FastAPI(
    title=Config.APP_NAME,
    description="A REST API for managing TODO items with Kubernetes deployment",
    version=Config.APP_VERSION,
    docs_url="/docs" if Config.ENABLE_DOCS else None,
    redoc_url="/redoc" if Config.ENABLE_DOCS else None,
)

# Include routers
app.include_router(root_router)
app.include_router(health_router)
app.include_router(todos_router)

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting FastAPI TODO Application")
    Config.log_config()
    
    # Add sample data if in development
    if Config.ENVIRONMENT == "development":
        logger.info("Adding sample TODO items for development")
        sample_todos = [
            TodoCreate(title="Learn FastAPI", description="Complete FastAPI tutorial", completed=True),
            TodoCreate(title="Learn Kubernetes", description="Master K8s concepts", completed=False),
            TodoCreate(title="Learn Helm", description="Deploy apps with Helm", completed=False),
        ]
        for todo in sample_todos:
            database.create_todo(todo)
        logger.info(f"Added {len(sample_todos)} sample TODO items")

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    from datetime import datetime
    from fastapi import status
    
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ============================================================================
# MAIN (for local testing)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting application with uvicorn")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=Config.DEBUG_MODE,
        log_level=LOG_LEVEL.lower()
    )
