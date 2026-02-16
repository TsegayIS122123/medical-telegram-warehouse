# src/database/queries.py
"""Database queries for analytics."""
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Dict, Any

def get_top_products(session: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get most frequently mentioned products.
    
    Note: This is a simplified version. In production, you'd use NLP.
    """
    result = session.execute(
        text("""
        SELECT 
            UNNEST(REGEXP_MATCHES(LOWER(message_text), '([a-z]+\\s?[a-z]+)', 'g')) as product,
            COUNT(*) as mention_count
        FROM marts.fct_messages
        WHERE message_text IS NOT NULL
        GROUP BY product
        ORDER BY mention_count DESC
        LIMIT :limit
        """),
        {"limit": limit}
    )
    return [{"product": row[0], "mentions": row[1]} for row in result]

def get_channel_activity(session: Session, channel_name: str) -> Dict[str, Any]:
    """Get posting activity for a channel."""
    result = session.execute(
        text("""
        SELECT 
            c.channel_name,
            COUNT(f.message_id) as total_posts,
            AVG(f.view_count) as avg_views,
            AVG(f.forward_count) as avg_forwards,
            COUNT(DISTINCT f.date_key) as active_days,
            SUM(CASE WHEN f.has_image THEN 1 ELSE 0 END) as posts_with_images
        FROM marts.fct_messages f
        JOIN marts.dim_channels c ON f.channel_key = c.channel_key
        WHERE c.channel_name = :channel_name
        GROUP BY c.channel_name
        """),
        {"channel_name": channel_name}
    )
    row = result.first()
    if not row:
        return {}
    return {
        "channel_name": row[0],
        "total_posts": row[1],
        "avg_views": float(row[2]) if row[2] else 0,
        "avg_forwards": float(row[3]) if row[3] else 0,
        "active_days": row[4],
        "posts_with_images": row[5]
    }

def search_messages(session: Session, query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Search for messages containing a keyword."""
    result = session.execute(
        text("""
        SELECT 
            f.message_id,
            c.channel_name,
            f.message_text,
            f.view_count,
            f.forward_count,
            f.has_image
        FROM marts.fct_messages f
        JOIN marts.dim_channels c ON f.channel_key = c.channel_key
        WHERE LOWER(f.message_text) LIKE LOWER(:query)
        ORDER BY f.view_count DESC
        LIMIT :limit
        """),
        {"query": f"%{query}%", "limit": limit}
    )
    return [
        {
            "message_id": row[0],
            "channel": row[1],
            "text": row[2][:200] + "..." if len(row[2]) > 200 else row[2],
            "views": row[3],
            "forwards": row[4],
            "has_image": row[5]
        }
        for row in result
    ]

def get_visual_content_stats(session: Session) -> Dict[str, Any]:
    """Get statistics about image usage."""
    result = session.execute(
        text("""
        SELECT 
            COUNT(DISTINCT message_id) as total_images,
            AVG(view_count) as avg_views_with_images,
            (SELECT AVG(view_count) FROM marts.fct_messages WHERE has_image = false) as avg_views_without_images,
            COUNT(DISTINCT channel_key) as channels_with_images
        FROM marts.fct_messages
        WHERE has_image = true
        """)
    )
    row = result.first()
    return {
        "total_images_analyzed": row[0],
        "avg_views_with_images": float(row[1]) if row[1] else 0,
        "avg_views_without_images": float(row[2]) if row[2] else 0,
        "impact_percentage": ((float(row[1] or 0) - float(row[2] or 0)) / float(row[2] or 1)) * 100 if row[2] else 0,
        "channels_with_images": row[3]
    }