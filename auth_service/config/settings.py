import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

AUTH_DATABASE_URL = os.environ.get("AUTH_DATABASE_URL")
JWT_SECRET = os.environ.get("JWT_SECRET")
TOKEN_EXPIRE_MINS = os.environ.get("TOKEN_EXPIRE_MINS")
