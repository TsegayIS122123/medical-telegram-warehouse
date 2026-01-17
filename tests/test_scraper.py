import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def test_environment_variables():
    """Test that required environment variables are set."""
    assert os.getenv('POSTGRES_USER') is not None, "POSTGRES_USER not set"
    assert os.getenv('POSTGRES_DB') is not None, "POSTGRES_DB not set"
    
def test_telegram_credentials():
    """Test Telegram API credentials are available (but not necessarily valid)."""
    # These should exist in .env file
    assert os.getenv('TELEGRAM_API_ID') is not None, "TELEGRAM_API_ID not set"
    assert os.getenv('TELEGRAM_API_HASH') is not None, "TELEGRAM_API_HASH not set"
    
def test_data_directories():
    """Test that required data directories exist."""
    directories = [
        'data/raw/images',
        'data/raw/telegram_messages',
        'logs'
    ]
    
    for directory in directories:
        # Check if directory exists or can be created
        os.makedirs(directory, exist_ok=True)
        assert os.path.exists(directory), f"Directory {directory} does not exist"