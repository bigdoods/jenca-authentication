import unittest
import tempfile

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
        signup = test_app.post('/users', data={})
        self.assertEqual(signup.headers['Content-Type'], 'application/json')

    def test_missing_username(self):
        pass


class LoginTests(unittest.TestCase):
    """
    Tests for logging in.
    """

if __name__ == '__main__':
    unittest.main()
