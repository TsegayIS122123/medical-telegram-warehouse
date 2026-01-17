import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings."""
    
    # Telegram API
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE')
    
    # PostgreSQL Database
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'warehouse_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'warehouse_pass')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'medical_warehouse')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    
    # Application
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
