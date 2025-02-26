"""
Type-validated settings for the Auth Service using Pydantic.

This module imports raw environment variables from settings.py and then
defines a Pydantic settings class that validates these values. This provides
an extra layer of type safety for critical configuration values.

Attributes:
    AUTH_DATABASE_URL (str): The URL for connecting to the authentication database.
    JWT_SECRET (str): The secret key used for encoding/decoding JWT tokens.
    TOKEN_EXPIRE_MINS (int): The number of minutes before a token expires.
"""

from pydantic_settings import BaseSettings
from auth_service.config.settings import AUTH_DATABASE_URL, JWT_SECRET, TOKEN_EXPIRE_MINS

class TypeSettings(BaseSettings):
    """Pydantic settings for type-validated configuration."""
    auth_database_url: str = AUTH_DATABASE_URL
    jwt_secret: str = JWT_SECRET
    token_expire_mins: int = int(TOKEN_EXPIRE_MINS) if TOKEN_EXPIRE_MINS is not None else 30

type_settings: TypeSettings = TypeSettings()

AUTH_DATABASE_URL: str = type_settings.auth_database_url
JWT_SECRET: str = type_settings.jwt_secret
TOKEN_EXPIRE_MINS: int = type_settings.token_expire_mins
