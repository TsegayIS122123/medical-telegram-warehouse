# api/schemas.py - Pydantic models
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Response models
class ChannelStats(BaseModel):
    channel_name: str
    channel_type: str
    total_messages: int
    avg_views: float
    messages_with_images: int
    image_percentage: float
    
    class Config:
        from_attributes = True

class TopProduct(BaseModel):
    product_term: str
    frequency: int
    channels: List[str]
    
    class Config:
        from_attributes = True

class Message(BaseModel):
    message_id: int
    channel_name: str
    message_date: datetime
    message_text: str
    views: int
    forwards: int
    has_image: bool
    
    class Config:
        from_attributes = True

class VisualContentStats(BaseModel):
    channel_name: str
    total_images: int
    promotional: int
    product_display: int
    lifestyle: int
    other: int
    promotional_percentage: float
    
    class Config:
        from_attributes = True

class ActivityTrend(BaseModel):
    date: str
    message_count: int
    avg_views: float
    
    class Config:
        from_attributes = True

# Request models
class MessageSearch(BaseModel):
    query: str
    limit: Optional[int] = 20
    channel: Optional[str] = None