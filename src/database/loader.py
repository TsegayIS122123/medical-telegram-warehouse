# src/database/loader.py
"""Load data into PostgreSQL."""
import json
from pathlib import Path
from typing import List, Dict, Any
import logging
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.config import config
from src.database.models import RawMessage, Base
from src.database.connection import get_engine, get_session

logger = logging.getLogger(__name__)

class DataLoader:
    """Load data from JSON files to PostgreSQL."""
    
    def __init__(self):
        self.engine = get_engine()
        self.config = config.database
        
    def create_schemas(self) -> None:
        """Create database schemas if they don't exist."""
        with self.engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS marts;"))
            conn.commit()
            
        # Create tables
        Base.metadata.create_all(self.engine)
        logger.info("Database schemas and tables created")
        
    def load_json_files(self, date: str) -> int:
        """
        Load all JSON files for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Number of messages loaded
        """
        json_dir = Path(f"data/raw/telegram_messages/{date}")
        
        if not json_dir.exists():
            logger.warning(f"No JSON files found for {date}")
            return 0
            
        total_loaded = 0
        
        with get_session() as session:
            for json_file in json_dir.glob("*.json"):
                with open(json_file, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    
                for msg_data in messages:
                    # Check if message already exists
                    existing = session.query(RawMessage).filter_by(
                        message_id=msg_data['message_id']
                    ).first()
                    
                    if not existing:
                        message = RawMessage(
                            message_id=msg_data['message_id'],
                            channel_name=msg_data['channel_name'],
                            message_date=msg_data['message_date'],
                            message_text=msg_data.get('message_text', ''),
                            has_media=msg_data.get('has_media', False),
                            image_path=msg_data.get('image_path'),
                            views=msg_data.get('views', 0),
                            forwards=msg_data.get('forwards', 0)
                        )
                        session.add(message)
                        total_loaded += 1
                        
            session.commit()
            
        logger.info(f"Loaded {total_loaded} messages for {date}")
        return total_loaded