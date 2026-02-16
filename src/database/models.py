# src/database/models.py
"""SQLAlchemy models for the database."""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class RawMessage(Base):
    """Raw message from Telegram."""
    __tablename__ = 'raw_telegram_messages'
    __table_args__ = {'schema': 'raw'}
    
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    channel_name = Column(String(255), nullable=False)
    message_date = Column(DateTime)
    message_text = Column(Text)
    has_media = Column(Boolean, default=False)
    image_path = Column(String(500))
    views = Column(Integer, default=0)
    forwards = Column(Integer, default=0)
    scraped_at = Column(DateTime, default=datetime.now)

class YOLODetection(Base):
    """YOLO detection results."""
    __tablename__ = 'yolo_detections'
    __table_args__ = {'schema': 'raw'}
    
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    channel_name = Column(String(255))
    image_path = Column(String(500))
    detected_class = Column(String(100))
    confidence_score = Column(Float)
    image_category = Column(String(50))
    detection_count = Column(Integer)
    detected_at = Column(DateTime)