# src/database/connection.py
"""Database connection management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import logging

from src.config import config

logger = logging.getLogger(__name__)

# Global engine instance
_engine = None

def get_engine():
    """Get or create database engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            config.database.connection_string,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True  # Check connection before using
        )
        logger.info(f"Database engine created for {config.database.host}:{config.database.port}")
    return _engine

def get_session() -> Session:
    """Get a new database session."""
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()