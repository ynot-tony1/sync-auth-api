from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from auth_service.config.settings import AUTH_DATABASE_URL
from auth_service.db.base import Base

engine = create_engine(AUTH_DATABASE_URL)

# sessionmaker returns a factory for new session objects
# binds the engine to every session so each one knows how to connect to the db
# the settings  make sure db changes arent commited automatically, so transactions can be managed with rollbacks
LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """
    Creates a new database session for a request.
    Using yield turns the function into a generator, allowing it to be used as a dependency by fast api.
    Once the request is done, the session is then closed.
    """
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


