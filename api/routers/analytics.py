# api/routers/analytics.py
"""Analytics endpoints."""
from fastapi import APIRouter, HTTPException
import logging

from src.database.connection import get_session
from src.database.queries import get_visual_content_stats

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/visual-content")
async def visual_content_stats():
    """Get statistics about image usage across channels."""
    try:
        with get_session() as session:
            stats = get_visual_content_stats(session)
            return stats
    except Exception as e:
        logger.error(f"Error fetching visual content stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))