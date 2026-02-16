# tests/conftest.py
"""Pytest configuration and fixtures."""
import pytest
import os
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

@pytest.fixture
def test_db_url():
    """Get test database URL."""
    return f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

@pytest.fixture
def sample_message():
    """Sample message data for testing."""
    return {
        'message_id': 12345,
        'channel_name': 'test_channel',
        'message_date': '2024-01-01T12:00:00',
        'message_text': 'Test message',
        'has_media': False,
        'views': 100,
        'forwards': 5
    }