from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime = None
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    message_id: int
    channel_name: str
    message_date: datetime
    message_text: str
    
class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    views: Optional[int] = None
    forwards: Optional[int] = None
    has_media: bool = False
    
    class Config:
        from_attributes = True
