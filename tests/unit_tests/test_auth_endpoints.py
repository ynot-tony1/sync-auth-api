"""
Unit Test Suite for Auth Service API Endpoints.

This module tests the /register and /login endpoints defined in
auth_service/routes/auth.py. It uses FastAPI's TestClient to simulate HTTP requests
and verifies the responses to ensure that user registration and login function as expected.
"""

import uuid
import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from auth_service.main import app


client = TestClient(app)

class TestAuthEndpoints(unittest.TestCase):
    """
    Tests for the /register and /login endpoints of the authentication service.
    """

    def setUp(self):
        """
        Set up test dependencies.

        Overrides the get_db dependency to supply a dummy database session for testing.
        This method is executed before each test method in the class.
        """
        self.dummy_db = MagicMock()
        app.dependency_overrides = {
            'get_db': lambda: iter([self.dummy_db])
        }

    def tearDown(self):
        """
        Tear down test dependencies.

        Removes any dependency overrides that were set during the tests.
        This method is executed after each test method in the class.
        """
        app.dependency_overrides = {}

    @patch("auth_service.routes.auth.get_user_by_email")
    @patch("auth_service.routes.auth.create_user")
    def test_register_new_user(self, mock_create_user, mock_get_user_by_email):
        """
        Test registration for a new user.

        This test confirms that registering a new user (when the email is not already used)
        returns a successful HTTP response (status code 200) along with a valid JWT in the
        response payload.

        Args:
            mock_create_user (MagicMock): Mocked create_user function to simulate user creation.
            mock_get_user_by_email (MagicMock): Mocked get_user_by_email function to simulate
                checking for existing users.
        """
        mock_get_user_by_email.return_value = None  
        fake_sub = str(uuid.uuid4())
        class FakeUser:
            def __init__(self):
                self.sub = fake_sub
                self.email = "synx@ttesting.com"

        fake_user = FakeUser()
        mock_create_user.return_value = fake_user  
        response = client.post("/register", json={"email": "synx@ttesting.com", "password": "testpass"})
        self.assertEqual(response.status_code, 200, "Registration should succeed for a new user.")
        data = response.json()
        self.assertIn("access_token", data, "Response must include an access token.")
        self.assertEqual(data.get("token_type"), "bearer", "Token type must be 'bearer'.")

    @patch("auth_service.routes.auth.get_user_by_email")
    def test_register_existing_user(self, mock_get_user_by_email):
        """
        Test registration for an existing user.

        This test confirms that attempting to register with an email that is already registered
        fails with a 400 error, and the response includes an error message indicating that the
        email is already registered.

        Args:
            mock_get_user_by_email (MagicMock): Mocked get_user_by_email function to simulate
                an existing user.
        """
        fake_user = object()
        mock_get_user_by_email.return_value = fake_user
        response = client.post("/register", json={"email": "synx@ttesting.com", "password": "testpass"})
        self.assertEqual(response.status_code, 400, "Registration must fail for an existing user.")
        data = response.json()
        self.assertEqual(
            data.get("detail"),
            "That email is already registered",
            "Error message should indicate the email is already registered."
        )

    @patch("auth_service.routes.auth.get_user_by_email")
    def test_login_success(self, mock_get_user_by_email):
        """
        Test successful login.

        This test verifies that providing valid credentials returns a 200 status code and a
        JSON payload containing a valid access token and a token type of 'bearer'.

        Args:
            mock_get_user_by_email (MagicMock): Mocked get_user_by_email function to simulate
                retrieving a user with matching credentials.
        """
        plain_password = "testpass"
        from auth_service.utils.security import hash_password
        hashed = hash_password(plain_password)

        class FakeUser:
            def __init__(self):
                self.sub = str(uuid.uuid4())
                self.email = "synx@ttesting.com"
                self.hashed_password = hashed

        fake_user = FakeUser()
        mock_get_user_by_email.return_value = fake_user  
        response = client.post("/login", json={"email": "synx@ttesting.com", "password": plain_password})
        self.assertEqual(response.status_code, 200, "Login should succeed for valid credentials.")
        data = response.json()
        self.assertIn("access_token", data, "Response must include an access token.")
        self.assertEqual(data.get("token_type"), "bearer", "Token type must be 'bearer'.")

    @patch("auth_service.routes.auth.get_user_by_email")
    def test_login_failure_wrong_password(self, mock_get_user_by_email):
        """
        Test login failure due to an incorrect password.

        This test confirms that if a user provides an incorrect password, the login attempt
        fails with a 400 error and an appropriate error message is returned.

        Args:
            mock_get_user_by_email (MagicMock): Mocked get_user_by_email function to simulate
                retrieving a user with a known password.
        """
        correct_password = "correctpass"
        from auth_service.utils.security import hash_password  
        hashed = hash_password(correct_password)

        class FakeUser:
            pass

        fake_user = FakeUser()
        fake_user.sub = str(uuid.uuid4())
        fake_user.email = "synx@ttesting.com"
        fake_user.hashed_password = hashed
        mock_get_user_by_email.return_value = fake_user
        response = client.post("/login", json={"email": "synx@ttesting.com", "password": "wrongpass"})
        self.assertEqual(response.status_code, 400, "Login must fail for an incorrect password.")
        data = response.json()
        self.assertEqual(
            data.get("detail"),
            "Invalid username or password",
            "Error message should indicate invalid credentials."
        )

    @patch("auth_service.routes.auth.get_user_by_email")
    def test_login_failure_no_user(self, mock_get_user_by_email):
        """
        Test login failure when the user does not exist.

        This test confirms that if the email provided is not registered, the login attempt
        fails with a 400 error and returns an appropriate error message indicating invalid credentials.

        Args:
            mock_get_user_by_email (MagicMock): Mocked get_user_by_email function to simulate
                a non-existent user.
        """
        mock_get_user_by_email.return_value = None
        response = client.post("/login", json={"email": "notarealthing@unreal.com", "password": "any"})
        self.assertEqual(response.status_code, 400, "Login must fail for a non-existent user.")
        data = response.json()
        self.assertEqual(
            data.get("detail"),
            "Invalid username or password",
            "Error message should indicate invalid credentials."
        )


if __name__ == "__main__":
    unittest.main()
