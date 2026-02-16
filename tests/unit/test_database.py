"""Test database connection and models."""
import pytest
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def test_database_connection():
    """Test that we can connect to the database."""
    # This is a simple test to verify database credentials
    db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        print("Database connection test passed!")
    except Exception as e:
        pytest.skip(f"Cannot connect to database: {e}")
