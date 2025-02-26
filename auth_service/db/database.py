"""
Database module for establishing the connection and session management.

This module creates the SQLAlchemy engine and session factory, and provides a dependency function
for obtaining a new database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from auth_service.config.type_settings import AUTH_DATABASE_URL
from auth_service.db.base import Base

engine = create_engine(AUTH_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Create and yield a new database session for a request.

    Yields:
        Session: A new SQLAlchemy session instance.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
