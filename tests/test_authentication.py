import json
import unittest

from requests import codes
from authentication import authentication


class SignupTests(unittest.TestCase):
    """
    Tests for the user sign up endpoint at ``/signup``.
    """

    def test_signup(self):
        """
        A signup request with a username and password returns a JSON response
        with user credentials and a CREATED status.
        """
        test_app = authentication.app.test_client()
        data = {'username': 'alice', 'password': 'secret'}
        response = test_app.post('/signup', data=data)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)
        self.assertEqual(json.loads(response.data), data)

    def test_missing_data(self):
        """
        A signup request without a username or password returns a BAD_REQUEST.
        """
        test_app = authentication.app.test_client()
        response = test_app.post('/signup', data={})
        self.assertEqual(response.status_code, codes.BAD_REQUEST)


class LoginTests(unittest.TestCase):
    """
    Tests for logging in.
    """

if __name__ == '__main__':
    unittest.main()
