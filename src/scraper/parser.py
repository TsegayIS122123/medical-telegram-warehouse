# src/scraper/parser.py
"""Message parsing logic."""
from typing import Dict, Any, Optional
from datetime import datetime
from telethon.tl.types import Message

class MessageParser:
    """Parse Telegram messages into structured format."""
    
    def parse_message(self, message: Message, channel: str) -> Dict[str, Any]:
        """
        Parse a Telegram message into a dictionary.
        
        Args:
            message: Telegram message object
            channel: Channel name
            
        Returns:
            Parsed message dictionary
        """
        return {
            'message_id': message.id,
            'channel_name': channel,
            'message_date': message.date.isoformat(),
            'message_text': message.text or '',
            'has_media': bool(message.media),
            'views': getattr(message, 'views', 0),
            'forwards': getattr(message, 'forwards', 0),
            'scraped_at': datetime.now().isoformat()
        }