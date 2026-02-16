# src/scraper/client.py
"""Telegram client wrapper for scraping messages."""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError
import random

from src.config import config
from src.scraper.parser import MessageParser
from src.scraper.utils import RateLimiter

logger = logging.getLogger(__name__)

class TelegramScraper:
    """Production-ready Telegram scraper with error handling and rate limiting."""
    
    def __init__(self):
        self.config = config.telegram
        self.parser = MessageParser()
        self.rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
        self.client = TelegramClient(
            'session/telegram_session',
            self.config.api_id,
            self.config.api_hash
        )
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.client.start(phone=self.config.phone)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.disconnect()
        
    async def scrape_channel(
        self, 
        channel: str, 
        days_back: int = 30,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Scrape messages from a Telegram channel.
        
        Args:
            channel: Channel username or link
            days_back: Number of days to look back
            limit: Maximum number of messages to scrape
            
        Returns:
            List of parsed message dictionaries
            
        Raises:
            Exception: If scraping fails
        """
        try:
            # Rate limiting
            await self.rate_limiter.wait_if_needed()
            
            # Get channel entity
            entity = await self.client.get_entity(channel)
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            messages = []
            async for message in self.client.iter_messages(
                entity,
                limit=limit,
                offset_date=datetime.now(),
                reverse=True
            ):
                if message.date < cutoff_date:
                    break
                    
                parsed = self.parser.parse_message(message, channel)
                messages.append(parsed)
                
                # Download image if present
                if message.media and hasattr(message.media, 'photo'):
                    await self._download_image(message, channel)
                    
            logger.info(f"Scraped {len(messages)} messages from {channel}")
            return messages
            
        except FloodWaitError as e:
            logger.warning(f"Rate limited, waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            return await self.scrape_channel(channel, days_back, limit)
            
        except Exception as e:
            logger.error(f"Failed to scrape {channel}: {e}")
            raise
            
    async def _download_image(self, message, channel: str) -> Optional[Path]:
        """
        Download image from message.
        
        Args:
            message: Telegram message with media
            channel: Channel name
            
        Returns:
            Path to downloaded image or None
        """
        try:
            # Create directory structure: data/raw/images/{channel}/{message_id}.jpg
            image_dir = Path(f"data/raw/images/{channel}")
            image_dir.mkdir(parents=True, exist_ok=True)
            
            image_path = image_dir / f"{message.id}.jpg"
            
            # Download if not exists
            if not image_path.exists():
                await message.download_media(str(image_path))
                logger.debug(f"Downloaded image: {image_path}")
                
            return image_path
            
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            return None
            
    async def scrape_all_channels(self) -> List[Dict[str, Any]]:
        """
        Scrape all configured channels.
        
        Returns:
            Combined list of messages from all channels
        """
        all_messages = []
        
        for channel in self.config.channels:
            try:
                messages = await self.scrape_channel(channel)
                all_messages.extend(messages)
                
                # Random delay between channels
                await asyncio.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Error scraping {channel}: {e}")
                continue
                
        return all_messages