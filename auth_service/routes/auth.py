import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.db_methods import get_user_by_email, create_user
from db.database import get_db
from utils.security import create_access_token, hash_password, verify_password
from models.user import UserRegister, UserLogin

router = APIRouter()


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Registers a new user in the authentication system.

    Takes a user registration model and a database session by FastAPI's dependency injection.
    First, it checks if a user with the provided email already exists in the 'auth_users' table.
    If a match is found, it responds with a HTTP 400 error, 'bad request'.
    If no user with that email is found, a sub is created with an uuid and the password is hashed.
    When the user is created, a JWT is created using the user's sub and email.
    The token and its type are then returned in the json.

    Args:
        user (UserRegister): The user registration data, email and password.
        db (Session): The database session provided by the dependency injection.

    Returns:
        dict: A dictionary containing the jwt as 'access_token' and the token type as 'bearer'.

    Raises:
        HTTPException 400 (bad request): Gets raised if a user with the provided email already exists.
    """
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="That email is already registered")
    new_sub = str(uuid.uuid4())
    hashed_pw = hash_password(user.password)
    auth_user = create_user(db, user.email, hashed_pw, new_sub)
    token = create_access_token({"sub": auth_user.sub, "email": auth_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Logs in an existing user by validating the provided credentials.

    This endpoint receives a user login model and a database session via FastAPI's dependency injection.
    It queries the 'auth_users' table to find a record that matches the email.
    If no user is found or if the provided password doesn't match the hashed password from the table,
    a HTTP 400 error is returned, 'bad request'.
    If the credentials are valid, a JWT access token is generated using the user's sub and email,
    and the token along with its type is returned in the JSON response.

    Args:
        user (UserLogin): The login credentials containing the email and password.
        db (Session): The database session provided via dependency injection.

    Returns:
        dict: A dictionary containing the generated JWT as 'access_token' and the token type as 'Bearer'.

    Raises:
        HTTPException 400 (bad request): This gets raised if no user is found or if the password is invalid.
    """
    auth_user = get_user_by_email(db, user.email)
    if not auth_user or not verify_password(user.password, auth_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token({"sub": auth_user.sub, "email": auth_user.email})
    return {"access_token": token, "token_type": "bearer"}
