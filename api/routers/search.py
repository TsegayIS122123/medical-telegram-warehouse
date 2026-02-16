# api/routers/search.py
"""Search endpoints."""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
import logging

from src.database.connection import get_session
from src.database.queries import search_messages

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/messages")
async def search_messages_endpoint(
    query: str = Query(..., description="Search keyword", min_length=2),
    limit: int = Query(20, description="Number of results to return", ge=1, le=100)
):
    """Search for messages containing a keyword."""
    try:
        with get_session() as session:
            results = search_messages(session, query, limit)
            return results
    except Exception as e:
        logger.error(f"Error searching messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))