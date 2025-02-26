"""
Database methods for the Auth Service.

This module provides functions to interact with the database such as retrieving
a user by email or creating a new user record.
"""

from typing import Optional
from sqlalchemy.orm import Session
from auth_service.models.user import AuthUser

def get_user_by_email(db: Session, email: str) -> Optional[AuthUser]:
    """Retrieve an AuthUser record by email.

    Args:
        db (Session): The database session.
        email (str): The email address to search for.

    Returns:
        Optional[AuthUser]: The AuthUser instance if found; otherwise, None.
    """
    return db.query(AuthUser).filter(AuthUser.email == email).first()

def create_user(db: Session, email: str, hashed_password: str, sub: str) -> AuthUser:
    """Create a new AuthUser record in the database.

    Args:
        db (Session): The database session.
        email (str): The user's email.
        hashed_password (str): The user's hashed password.
        sub (str): A unique subject identifier for the user.

    Returns:
        AuthUser: The newly created AuthUser record.
    """
    new_user = AuthUser(email=email, hashed_password=hashed_password, sub=sub)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
