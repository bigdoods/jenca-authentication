import unittest

from requests import codes
from authentication import authentication


class SignupTests(unittest.TestCase):
    """
    Signup tests.
    """

    def test_signup(self):
        """
        Test that a valid signup request returns an OK status.
        """
        test_app = authentication.app.test_client()
        response = test_app.get('/login')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.ok)

    def test_missing_username(self):
        pass


class LoginTests(unittest.TestCase):
    """
    Tests for logging in.
    """

if __name__ == '__main__':
    unittest.main()
