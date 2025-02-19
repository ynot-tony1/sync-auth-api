from sqlalchemy.orm import Session
from models.user import AuthUser

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user from the database by their email address.

    Function queries the 'auth_users' table using the AuthUser model to find a record
    that matches the provided email. If a matching record is found, the corresponding
    AuthUser object is returned. Otherwise, None is returned.

    Args:
        db (Session): The SQLAlchemy database session.
        email (str): The email address of the user to search for.

    Returns:
        Optional[AuthUser]: The AuthUser record if found, otherwise None.
    """
    query = db.query(AuthUser)
    filtered_query = query.filter(AuthUser.email == email)
    user = filtered_query.first()
    return user



def create_user(db: Session, email, hashed_password, sub):
    """
    Creates a new AuthUser entry in the database.

    First an instance of the AuthUser model is created with the values that are passed in.
    This instance of auth user is marked as pending to be put in and then committed.
    The table entry in the database is reloaded, which would then show auto generated fields like pks or default values.
    A new user object is returned if it is successful. If an error occurs, the whole SQL transaction would be rolled back.

    Args:
        db (Session): The SQLAlchemy database session.
        email (str): The email address for the new user.
        hashed_password (str): The hashed password for the new user.
        sub (str): A unique identifier for the new user.

    Returns:
        AuthUser: The newly created auth user object.

    Raises:
        Exception: If an error occurs during the transaction, the transaction is rolled back and the exception is re-raised.
    """
    try:
        auth_user = AuthUser(email=email, hashed_password=hashed_password, sub=sub)
        db.add(auth_user)
        db.commit()
        db.refresh(auth_user)
        return auth_user
    except Exception as e:
        db.rollback()  
        raise e
