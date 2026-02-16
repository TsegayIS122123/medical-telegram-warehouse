# api/routers/products.py
"""Product-related endpoints."""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
import logging

from src.database.connection import get_session
from src.database.queries import get_top_products

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/top-products")
async def top_products(
    limit: int = Query(10, description="Number of products to return", ge=1, le=100)
):
    """Get most frequently mentioned products."""
    try:
        with get_session() as session:
            products = get_top_products(session, limit)
            return products
    except Exception as e:
        logger.error(f"Error fetching top products: {e}")
        raise HTTPException(status_code=500, detail=str(e))