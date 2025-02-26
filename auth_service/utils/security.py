"""
Security utilities module.

This module provides functions for generating JWT access tokens,
hashing passwords, and verifying passwords using bcrypt.
"""

import time
import jwt
import bcrypt
from typing import Dict, Any
from auth_service.config.type_settings import JWT_SECRET, TOKEN_EXPIRE_MINS

def create_access_token(data: Dict[str, Any]) -> str:
    """Creates a JWT access token with an expiration time.

    Args:
        data (Dict[str, Any]): The payload data for the JWT.

    Returns:
        str: The encoded JWT token.
    """
    seconds_until_expiry: int = int(TOKEN_EXPIRE_MINS) * 60
    now: int = int(time.time())
    exp_timestamp: int = now + seconds_until_expiry
    data["exp"] = exp_timestamp
    return jwt.encode(data, JWT_SECRET, algorithm="HS256")

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The resulting hashed password.
    """
    hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password.

    Args:
        password (str): The plaintext password to verify.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches; otherwise, False.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
