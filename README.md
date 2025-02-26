# Auth Service

The Auth Service is a FastAPI-based authentication API that provides endpoints for user registration and login.
It leverages SQLAlchemy for database interactions, bcrypt for secure password hashing, and JWT for token-based authentication.

## Features

- **User Registration:** Create new users with unique email addresses.
- **User Login:** Authenticate users using hashed passwords.
- **JWT Authentication:** Generates JSON Web Tokens with expiration.
- **Database Management:** Uses SQLAlchemy ORM for interacting with a PostgreSQL database.
- **CORS Support:** Configured middleware to support cross-origin requests.

## Directory Structure

auth_service
├── config
│   ├── __init__.py
│   ├── settings.py
│   └── type_settings.py
├── db
│   ├── base.py
│   ├── database.py
│   ├── db_methods.py
│   └── __init__.py
├── main.py
├── models
│   ├── __init__.py
│   └── user.py
├── routes
│   ├── auth.py
│   └── __init__.py
└── utils
    ├── __init__.py
    └── security.py

## Environment Variables

Before running the service, configure the following environment variables:

- **AUTH_DATABASE_URL**  
  Example: `postgresql://auth_admin:dbpass@localhost/auth_db`
- **JWT_SECRET**  
  Example: `supersecretkey`
- **TOKEN_EXPIRE_MINS**  
  Example: `30`

You can set these in your shell or use a `.env` file for local development.

## Setting the PYTHONPATH

Ensure that the PYTHONPATH is set to include the project root so that the modules can be correctly imported. You can do this manually in your shell:

- **On Linux/Mac:**

  ```bash
  export PYTHONPATH=$(pwd)

    On Windows (Command Prompt):

    set PYTHONPATH=%cd%

You can add these commands to your shell profile (e.g., .bashrc or .zshrc) for convenience.

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ynot-tony1/sync-auth-api.git
   cd auth_service

2. **Create a virtual environment:**

python -m venv venv
source venv/bin/activate  
On Windows: venv\Scripts\activate

3. **Install the dependencies:**

    pip install -r requirements.txt

4. **Configure Environment Variables:**

    Either export the variables manually or create a .env file in the project root with the required settings.

5. **Running the Application**

Start the FastAPI server using Uvicorn:

uvicorn main:app --reload --port 8000

Access the API at http://localhost:8000.

## Running Tests

Ensure that your PYTHONPATH is correctly set then execute:

python -m unittest discover -s tests/unit_tests -p "test_*.py" -v

## API Endpoints

POST /register

    Description: Registers a new user.
    Request Body: JSON with the following properties:
        email (string): User's email address.
        password (string): Plaintext password.
    Response: A JSON object containing:
        access_token: JWT token.
        token_type: Always "bearer".
    Error: Returns a 400 error if the email is already registered.

POST /login

    Description: Authenticates an existing user.
    Request Body: JSON with the following properties:
        email (string): User's email address.
        password (string): Plaintext password.
    Response: A JSON object containing:
        access_token: JWT token.
        token_type: Always "bearer".
    Error: Returns a 400 error if the credentials are invalid.

## Code Overview

    main.py:
        Initializes the FastAPI app.
        Configures CORS middleware.
        Includes the auth router and creates database tables on startup.

    config/
        Contains application configuration and settings.

    db/
        database.py: Sets up the SQLAlchemy engine and session factory.
        db_methods.py: Provides database helper functions (e.g., retrieving and creating users).
        base.py: Defines the base for SQLAlchemy models.

    models/user.py:
        Defines the SQLAlchemy model AuthUser for storing user details.
        Contains Pydantic models UserRegister and UserLogin for input validation.

    routes/auth.py:
        Implements the /register and /login endpoints.
        Utilizes dependency injection to manage database sessions.

    utils/security.py:
        Implements password hashing and verification using bcrypt.
        Provides JWT token generation with expiration.


## Dependencies

The project relies on several key Python packages:

    FastAPI: Web framework for building APIs.
    SQLAlchemy: ORM for database interactions.
    Pydantic: Data validation.
    bcrypt: Password hashing.
    PyJWT: JWT token encoding.
    uvicorn: ASGI server for FastAPI.
    (See requirements.txt for the full list of dependencies.)

## Additional Notes

    Database: Ensure the PostgreSQL database specified in AUTH_DATABASE_URL is running and accessible.
    JWT Tokens: Tokens are set to expire based on the TOKEN_EXPIRE_MINS value.
    Security Considerations: This service uses basic security measures and may require additional enhancements (e.g., rate limiting, HTTPS) for production deployment.
