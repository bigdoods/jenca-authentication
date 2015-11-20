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
        data = {'username': 'alice', 'password': 'secret'}
        response = test_app.post('/signup', data=data)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)

    def test_missing_username(self):
        test_app = authentication.app.test_client()
        data = {'password': 'secret'}
        response = test_app.post('/signup', data=data)
        self.assertEqual(response.status_code, codes.BAD_REQUEST)


class LoginTests(unittest.TestCase):
    """
    Tests for logging in.
    """

if __name__ == '__main__':
    unittest.main()
