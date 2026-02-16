# api/routers/channels.py
"""Channel-related endpoints."""
from fastapi import APIRouter, Path, HTTPException
import logging

from src.database.connection import get_session
from src.database.queries import get_channel_activity

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{channel_name}/activity")
async def channel_activity(
    channel_name: str = Path(..., description="Name of the Telegram channel")
):
    """Get posting activity for a specific channel."""
    try:
        with get_session() as session:
            activity = get_channel_activity(session, channel_name)
            if not activity:
                raise HTTPException(status_code=404, detail=f"Channel {channel_name} not found")
            return activity
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching channel activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))