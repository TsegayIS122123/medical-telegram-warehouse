# src/config.py
"""Configuration management using dataclasses and environment variables."""
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class TelegramConfig:
    """Telegram API configuration."""
    api_id: int
    api_hash: str
    phone: str
    channels: List[str] = field(default_factory=lambda: [
        'chemed',
        'lobelia4cosmetics',
        'tikvahpharma'
    ])
    
    @classmethod
    def from_env(cls) -> 'TelegramConfig':
        """Create config from environment variables."""
        return cls(
            api_id=int(os.getenv('TELEGRAM_API_ID', '0')),
            api_hash=os.getenv('TELEGRAM_API_HASH', ''),
            phone=os.getenv('TELEGRAM_PHONE', ''),
        )

@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    host: str
    port: int
    database: str
    user: str
    password: str
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create config from environment variables."""
        return cls(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', '5433')),
            database=os.getenv('POSTGRES_DB', 'medical_warehouse'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres')
        )
    
    @property
    def connection_string(self) -> str:
        """Get SQLAlchemy connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    @property
    def psycopg2_connection_string(self) -> str:
        """Get psycopg2 connection string."""
        return f"host={self.host} port={self.port} dbname={self.database} user={self.user} password={self.password}"

@dataclass
class YOLOConfig:
    """YOLO detection configuration."""
    model_path: Path = Path('yolov8n.pt')
    confidence_threshold: float = 0.5
    device: str = 'cpu'
    
    @classmethod
    def from_env(cls) -> 'YOLOConfig':
        """Create config from environment variables."""
        return cls(
            model_path=Path(os.getenv('YOLO_MODEL_PATH', 'yolov8n.pt')),
            confidence_threshold=float(os.getenv('YOLO_CONFIDENCE', '0.5')),
            device=os.getenv('YOLO_DEVICE', 'cpu')
        )

@dataclass
class AppConfig:
    """Main application configuration."""
    telegram: TelegramConfig = field(default_factory=TelegramConfig.from_env)
    database: DatabaseConfig = field(default_factory=DatabaseConfig.from_env)
    yolo: YOLOConfig = field(default_factory=YOLOConfig.from_env)
    environment: str = os.getenv('ENVIRONMENT', 'development')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def is_development(self) -> bool:
        """Check if in development mode."""
        return self.environment == 'development'
    
    @property
    def is_production(self) -> bool:
        """Check if in production mode."""
        return self.environment == 'production'

# Global config instance
config = AppConfig()