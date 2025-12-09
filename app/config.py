import os
import logging

logger = logging.getLogger(__name__)


class Config:
    """Application configuration from environment variables and ConfigMap"""
    
    # Application settings
    APP_NAME = os.getenv("APP_NAME", "FastAPI TODO Service")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Feature flags
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    ENABLE_DOCS = os.getenv("ENABLE_DOCS", "true").lower() == "true"
    MAX_ITEMS = int(os.getenv("MAX_ITEMS", "100"))
    
    @classmethod
    def log_config(cls):
        """Log configuration (hide sensitive data)"""
        logger.info("=" * 60)
        logger.info("APPLICATION CONFIGURATION")
        logger.info("=" * 60)
        logger.info(f"App Name: {cls.APP_NAME}")
        logger.info(f"Version: {cls.APP_VERSION}")
        logger.info(f"Environment: {cls.ENVIRONMENT}")
        logger.info(f"Debug Mode: {cls.DEBUG_MODE}")
        logger.info(f"Enable Docs: {cls.ENABLE_DOCS}")
        logger.info(f"Max Items: {cls.MAX_ITEMS}")
        logger.info("=" * 60)
