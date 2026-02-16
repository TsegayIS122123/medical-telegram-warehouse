import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def test_environment_variables():
    """Test that required environment variables are set."""
    assert os.getenv('POSTGRES_USER') is not None, "POSTGRES_USER not set"
    assert os.getenv('POSTGRES_DB') is not None, "POSTGRES_DB not set"

def test_telegram_credentials():
    """Test Telegram API credentials are available."""
    # Check for bot token (new method) OR API credentials (old method)
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    
    # Either bot token OR API credentials should be available
    assert bot_token is not None or (api_id is not None and api_hash is not None), \
        "Either TELEGRAM_BOT_TOKEN or TELEGRAM_API_ID/TELEGRAM_API_HASH must be set"

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
