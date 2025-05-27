"""
Module for SQLAlchemy and Pydantic models for the authentication user.

This module defines the SQLAlchemy ORM model for an authentication user and the corresponding
Pydantic models for request validation.
"""

from sqlalchemy import Column, Integer, String
from auth_service.db.database import Base
from pydantic import BaseModel

class AuthUser(Base):
    """SQLAlchemy model representing a user in the authentication system.

    Attributes:
        __tablename__ (str): Name of the database table.
        user_id (int): Primary key for the user record.
        email (str): Unique email address of the user.
        hashed_password (str): Hashed password of the user.
        sub (str): Unique subject identifier for the user.
    """
    __tablename__ = "auth_users"  
    user_id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    sub: str = Column(String, unique=True, nullable=False)

class UserRegister(BaseModel):
    """Pydantic model for user registration input.

    Attributes:
        email (str): User's email address.
        password (str): Plaintext password for registration.
    """
    email: str 
    password: str

class UserLogin(BaseModel):
    """Pydantic model for user login input.

    Attributes:
        email (str): User's email address.
        password (str): Plaintext password for login.
    """
    email: str
    password: str
