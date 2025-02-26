"""
Authentication routes module.

This module defines endpoints for user registration and login. It uses dependency injection
to provide database sessions and leverages Pydantic models for input validation.
"""

import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from auth_service.db.db_methods import get_user_by_email, create_user
from auth_service.db.database import get_db
from auth_service.utils.security import create_access_token, hash_password, verify_password
from auth_service.models.user import UserRegister, UserLogin

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Registers a new user in the authentication system.

    Args:
        user (UserRegister): The user registration data, containing email and password.
        db (Session): The database session provided by dependency injection.

    Returns:
        Dict[str, str]: A dictionary containing the JWT as 'access_token' and the token type as 'bearer'.

    Raises:
        HTTPException: If a user with the provided email already exists.
    """
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="That email is already registered")
    new_sub: str = str(uuid.uuid4())
    hashed_pw: str = hash_password(user.password)
    auth_user = create_user(db, user.email, hashed_pw, new_sub)
    token: str = create_access_token({"sub": auth_user.sub, "email": auth_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Logs in an existing user by validating the provided credentials.

    Args:
        user (UserLogin): The login credentials containing email and password.
        db (Session): The database session provided via dependency injection.

    Returns:
        Dict[str, str]: A dictionary containing the generated JWT as 'access_token' and the token type as 'bearer'.

    Raises:
        HTTPException: If the user is not found or the password is invalid.
    """
    auth_user = get_user_by_email(db, user.email)
    if not auth_user or not verify_password(user.password, auth_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token: str = create_access_token({"sub": auth_user.sub, "email": auth_user.email})
    return {"access_token": token, "token_type": "bearer"}
