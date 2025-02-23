"""
It contains two sets of models:

1.  AuthUser model is an SQLAlchemy ORM model that stands for a user record in the
   'auth_users' table. This model is used by the ORM to map python objects to database rows.
   It has fields for the user ID pk, email, hashed password, and a unique sub to identify it accross environments.

2. Pydantic models UserRegister and UserLogin are used to validate and organize
   input data for user registration and login. They make sure that the data coming into the API
   conforms to the expected structure for creating or authenticating users.

Classes:
    AuthUser: Inherits from the SQLAlchemy Base class. Outlines the structure of the 'auth_users'
    table with columns for user_id, email, hashed_password, and sub.

    UserRegister: A Pydantic BaseModel that requires an email and a password. 
    For validating registration data.

    UserLogin: A Pydantic BaseModel that requires an email and a password. For validating
               login data.
"""
from sqlalchemy import Column, Integer, String
from auth_service.db.database import Base
from pydantic import BaseModel

class AuthUser(Base):
    __tablename__ = "auth_users"  
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    sub = Column(String, unique=True, nullable=False)

class UserRegister(BaseModel):
    email: str 
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
