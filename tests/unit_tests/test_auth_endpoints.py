"""
Unit Test Suite for Auth Service API Endpoints

This module tests the /register and /login endpoints defined in auth_service/routes/auth.py.
"""

import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # Force in-memory SQLite for testing


import uuid
import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient



from auth_service.main import app

client = TestClient(app)

class TestAuthEndpoints(unittest.TestCase):
    """
    Tests for the /register and /login endpoints.
    """

    def setUp(self):
        """
        Overrides the get_db dependency to supply a dummy database session.
        """
        self.dummy_db = MagicMock()
        app.dependency_overrides = {
            'get_db': lambda: iter([self.dummy_db])
        }

    def tearDown(self):
        """
        Removes dependency overrides.
        """
        app.dependency_overrides = {}

    @patch("auth_service.routes.auth.get_user_by_email")
    @patch("auth_service.routes.auth.create_user")
    def test_register_new_user(self, mock_create_user, mock_get_user_by_email):
        """
        Confirming new user registration returns a valid JWT when the email is not used.
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
        Confirming registration fails when the email is already registered.
        """
        fake_user = object()
        mock_get_user_by_email.return_value = fake_user
        response = client.post("/register", json={"email": "synx@ttesting.com", "password": "testpass"})
        self.assertEqual(response.status_code, 400, "Registration must fail for an existing user.")
        data = response.json()
        self.assertEqual(data.get("detail"), "That email is already registered",
                        "Error message should indicate the email is already registered.")


    @patch("auth_service.routes.auth.get_user_by_email")
    def test_login_success(self, mock_get_user_by_email):
        """
        Confirming login returns a valid JWT for correct credentials.
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
        Confirming login fails with a 400 error for an incorrect password.
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
        self.assertEqual(data.get("detail"), "Invalid username or password",
                         "Error message should indicate invalid credentials.")

    @patch("auth_service.routes.auth.get_user_by_email")
    def test_login_failure_no_user(self, mock_get_user_by_email):
        """
        Confirming login fails with a 400 error when the email is not registered.
        """
        mock_get_user_by_email.return_value = None
        response = client.post("/login", json={"email": "notarealthing@unreal.com", "password": "any"})
        self.assertEqual(response.status_code, 400, "Login must fail for a non-existent user.")
        data = response.json()
        self.assertEqual(data.get("detail"), "Invalid username or password",
                         "Error message should indicate invalid credentials.")


if __name__ == "__main__":
    unittest.main()

