"""
Main application module for Auth Serivce.

This module creates and configures a FastAPI application instance.cIt applies CORS middleware 
to allow cross-origin requests. Includes the auth router and sets up the database schema by creating
any missing tables defined in the ORM's Base metadata.

To use:
    To run it, use a command like:
    uvicorn main:app --reload --port (port number)

Attributes:
    app (FastAPI): The FastAPI application instance.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from routes import auth

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
Base.metadata.create_all(bind=engine)
