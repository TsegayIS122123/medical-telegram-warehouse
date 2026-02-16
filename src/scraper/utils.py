# src/scraper/utils.py
"""Utility functions for scraper."""
import asyncio
import time
from typing import Optional

class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, max_calls: int, period: float):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum calls allowed in period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        
    async def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded."""
        now = time.time()
        
        # Remove old calls
        self.calls = [t for t in self.calls if now - t < self.period]
        
        if len(self.calls) >= self.max_calls:
            # Wait until oldest call expires
            wait_time = self.period - (now - self.calls[0])
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                
        self.calls.append(now)