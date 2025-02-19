import jwt
import time
import bcrypt
from config.settings import JWT_SECRET, TOKEN_EXPIRE_MINS

def create_access_token(data):
    """
    Creates a JWT access token with an expiration time.

    This function takes a dictionary containing the data for a JWT payload.
    It calculates an expiration timestamp based on the TOKEN_EXPIRE_MINS setting which is converted to seconds,
    and then encodes the payload into a JWT token using the provided secret.

    Args:
        data (dict): The payload data for the JWT.

    Returns:
        str: The JWT token.
    """
    seconds_until_expiry = int(TOKEN_EXPIRE_MINS) * 60
    now = int(time.time())
    exp_timestamp = now + seconds_until_expiry
    data["exp"] = exp_timestamp
    return jwt.encode(data, JWT_SECRET, algorithm="HS256")



def hash_password(password):
    """
    Hashes a password using bcrypt.

    This function converts the password into a UTF-8 encoded bytes object,
    which is required by bcrypt for hashing. It then hashes it using a generated salt,
    and then converts the resulting hash back into a string.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password as a string.
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password, hashed_password):
    """
    Verifies a password against a hashed password.

    This function converts the given password and the hashed password into 
    UTF-8. It then uses bcrypt to extract the salt and hash params from the stored hash, 
    hash the incoming password and compare the two of them.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, otherwise False.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
