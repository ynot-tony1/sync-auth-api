"""
Unit Test Suite for Auth Service Security Utilities

This module tests the functions defined in auth_service/utils/security.py,
which include JWT token creation (with an expiration claim), password hashing,
and password verification.
"""

import time
import jwt
import unittest
from auth_service.utils.security import create_access_token, hash_password, verify_password

class TestSecurityUtilities(unittest.TestCase):
    """
    Tests for the security utility functions.
    """

    def test_create_access_token_contains_expiry(self):
        """
        Ensure create_access_token embeds an 'exp' field with a future timestamp.
        """
        payload = {"sub": "12345", "email": "synced@inthenameof.com"}
        token = create_access_token(payload.copy())
        decoded = jwt.decode(token, options={"verify_signature": False})
        self.assertIn("exp", decoded, "Token must include an 'exp' claim.")
        self.assertGreater(decoded["exp"], int(time.time()),
                           "The 'exp' claim must be set to a future timestamp.")

    def test_hash_and_verify_password(self):
        """
        Validate that a hashed password verifies correctly and rejects incorrect passwords.
        """
        plain_password = "mysecretpassword"
        hashed = hash_password(plain_password)
        self.assertTrue(verify_password(plain_password, hashed),
                        "Correct password should verify against the hash.")
        self.assertFalse(verify_password("wrongpassword", hashed),
                         "Incorrect password should not verify against the hash.")


if __name__ == "__main__":
    unittest.main()
