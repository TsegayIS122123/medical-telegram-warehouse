# api/main.py
"""FastAPI application for Medical Telegram Warehouse."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from sqlalchemy import text

from src.config import config
from api.routers import products, channels, analytics, search

# Setup logging
logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="API for accessing Ethiopian medical Telegram channel analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/reports", tags=["reports"])
app.include_router(channels.router, prefix="/api/channels", tags=["channels"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Medical Telegram Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "reports": "/api/reports/top-products",
            "channels": "/api/channels/{channel_name}/activity",
            "search": "/api/search/messages?query=paracetamol"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    try:
        from src.database.connection import get_engine
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # FIXED: added text()
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        logger.error(f"Database health check failed: {e}")
    
    return {
        "status": "healthy",
        "database": db_status,
        "environment": config.environment
    }