# api/main.py - COMPLETE FASTAPI APPLICATION
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, func, case
from typing import List, Optional
import pandas as pd

from database import get_db
from schemas import (
    ChannelStats, TopProduct, Message, 
    VisualContentStats, ActivityTrend, MessageSearch
)

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytical API for Ethiopian Medical Telegram Data",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Medical Telegram Analytics API",
        "endpoints": {
            "reports": {
                "top_products": "/api/reports/top-products",
                "visual_content": "/api/reports/visual-content"
            },
            "channels": "/api/channels/{channel_name}/activity",
            "search": "/api/search/messages",
            "docs": "/docs"
        }
    }

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def get_top_products(
    limit: int = Query(10, description="Number of top products to return"),
    db: Session = Depends(get_db)
):
    """
    Get most frequently mentioned medical products across all channels.
    Extracts product terms from message text.
    """
    try:
        query = """
        WITH product_terms AS (
            SELECT 
                UNNEST(ARRAY['paracetamol', 'amoxicillin', 'vitamin', 'sanitizer', 
                       'mask', 'cream', 'tablet', 'capsule', 'injection', 'syrup',
                       'thermometer', 'monitor', 'kit', 'powder', 'drop']) as product
        ),
        message_counts AS (
            SELECT 
                pt.product,
                COUNT(DISTINCT fm.message_id) as frequency,
                ARRAY_AGG(DISTINCT dc.channel_name) as channels
            FROM product_terms pt
            CROSS JOIN public_marts.fct_messages fm
            JOIN public_marts.dim_channels dc ON fm.channel_key = dc.channel_key
            WHERE LOWER(fm.message_text) LIKE '%' || pt.product || '%'
            GROUP BY pt.product
            HAVING COUNT(DISTINCT fm.message_id) > 0
        )
        SELECT 
            product as product_term,
            frequency,
            channels
        FROM message_counts
        ORDER BY frequency DESC
        LIMIT :limit
        """
        
        result = db.execute(text(query), {"limit": limit})
        products = []
        
        for row in result:
            products.append({
                "product_term": row[0],
                "frequency": row[1],
                "channels": row[2] if row[2] else []
            })
        
        return products
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_name}/activity", response_model=List[ActivityTrend])
def get_channel_activity(
    channel_name: str,
    days: int = Query(7, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get posting activity and trends for a specific channel.
    Shows daily message counts and average views.
    """
    try:
        query = """
        SELECT 
            TO_CHAR(dd.full_date, 'YYYY-MM-DD') as date,
            COUNT(fm.message_id) as message_count,
            COALESCE(AVG(fm.view_count), 0) as avg_views
        FROM public_marts.dim_dates dd
        LEFT JOIN public_marts.fct_messages fm ON dd.date_key = fm.date_key
        LEFT JOIN public_marts.dim_channels dc ON fm.channel_key = dc.channel_key
        WHERE dc.channel_name = :channel_name
          AND dd.full_date >= CURRENT_DATE - INTERVAL ':days days'
        GROUP BY dd.full_date
        ORDER BY dd.full_date DESC
        """
        
        result = db.execute(text(query), {
            "channel_name": channel_name,
            "days": days
        })
        
        trends = []
        for row in result:
            trends.append({
                "date": row[0],
                "message_count": row[1] or 0,
                "avg_views": float(row[2] or 0)
            })
        
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/messages", response_model=List[Message])
def search_messages(
    query: str = Query(..., description="Search keyword"),
    limit: int = Query(20, description="Maximum results"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    db: Session = Depends(get_db)
):
    """
    Search for messages containing specific keywords.
    Supports channel filtering.
    """
    try:
        base_query = """
        SELECT 
            fm.message_id,
            dc.channel_name,
            dd.full_date as message_date,
            fm.message_text,
            fm.view_count as views,
            fm.forward_count as forwards,
            fm.has_image
        FROM public_marts.fct_messages fm
        JOIN public_marts.dim_channels dc ON fm.channel_key = dc.channel_key
        JOIN public_marts.dim_dates dd ON fm.date_key = dd.date_key
        WHERE LOWER(fm.message_text) LIKE '%' || LOWER(:query) || '%'
        """
        
        params = {"query": query, "limit": limit}
        
        if channel:
            base_query += " AND dc.channel_name = :channel"
            params["channel"] = channel
        
        base_query += " ORDER BY fm.view_count DESC LIMIT :limit"
        
        result = db.execute(text(base_query), params)
        
        messages = []
        for row in result:
            messages.append({
                "message_id": row[0],
                "channel_name": row[1],
                "message_date": row[2],
                "message_text": row[3],
                "views": row[4],
                "forwards": row[5],
                "has_image": row[6]
            })
        
        return messages
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/visual-content", response_model=List[VisualContentStats])
def get_visual_content_stats(db: Session = Depends(get_db)):
    """
    Get statistics about image usage and categorization across channels.
    Shows YOLO detection results by category.
    """
    try:
        # First check if YOLO table exists
        check_query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public_marts' 
            AND table_name = 'fct_image_detections'
        )
        """
        
        yolo_exists = db.execute(text(check_query)).scalar()
        
        if not yolo_exists:
            # Fallback to basic image stats
            query = """
            SELECT 
                dc.channel_name,
                COUNT(fm.message_id) as total_messages,
                SUM(CASE WHEN fm.has_image THEN 1 ELSE 0 END) as total_images,
                ROUND(100.0 * SUM(CASE WHEN fm.has_image THEN 1 ELSE 0 END) / COUNT(fm.message_id), 2) as image_percentage
            FROM public_marts.fct_messages fm
            JOIN public_marts.dim_channels dc ON fm.channel_key = dc.channel_key
            GROUP BY dc.channel_name
            ORDER BY total_images DESC
            """
            
            result = db.execute(text(query))
            
            stats = []
            for row in result:
                stats.append({
                    "channel_name": row[0],
                    "total_images": row[2] or 0,
                    "promotional": 0,
                    "product_display": 0,
                    "lifestyle": 0,
                    "other": 0,
                    "promotional_percentage": 0.0
                })
            
            return stats
        else:
            # Full YOLO analysis
            query = """
            SELECT 
                dc.channel_name,
                COUNT(fid.message_id) as total_images,
                SUM(CASE WHEN fid.image_category = 'promotional' THEN 1 ELSE 0 END) as promotional,
                SUM(CASE WHEN fid.image_category = 'product_display' THEN 1 ELSE 0 END) as product_display,
                SUM(CASE WHEN fid.image_category = 'lifestyle' THEN 1 ELSE 0 END) as lifestyle,
                SUM(CASE WHEN fid.image_category = 'other' THEN 1 ELSE 0 END) as other,
                ROUND(100.0 * SUM(CASE WHEN fid.image_category = 'promotional' THEN 1 ELSE 0 END) / 
                      NULLIF(COUNT(fid.message_id), 0), 2) as promotional_percentage
            FROM public_marts.fct_image_detections fid
            JOIN public_marts.dim_channels dc ON fid.channel_key = dc.channel_key
            GROUP BY dc.channel_name
            ORDER BY total_images DESC
            """
            
            result = db.execute(text(query))
            
            stats = []
            for row in result:
                stats.append({
                    "channel_name": row[0],
                    "total_images": row[1] or 0,
                    "promotional": row[2] or 0,
                    "product_display": row[3] or 0,
                    "lifestyle": row[4] or 0,
                    "other": row[5] or 0,
                    "promotional_percentage": float(row[6] or 0)
                })
            
            return stats
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)