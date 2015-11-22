import json
import unittest

from requests import codes

from authentication.authentication import app, db

# TODO Put this in a temporary test folder
SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/unit_test.db"

USER_DATA = {'email': 'alice@example.com', 'password': 'secret'}


class SignupTests(unittest.TestCase):
    """
    Tests for the user sign up endpoint at ``/signup``.
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def test_signup(self):
        """
        A signup request with a username and password returns a JSON response
        with user credentials and a CREATED status.
        """
        response = self.app.post('/signup', data=USER_DATA)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)
        self.assertEqual(json.loads(response.data.decode('utf8')), USER_DATA)

    def test_missing_data(self):
        """
        A signup request without a username or password returns a BAD_REQUEST.
        """
        response = self.app.post('/signup', data={})
        self.assertEqual(response.status_code, codes.BAD_REQUEST)

    def test_existing_user(self):
        """
        """
        self.app.post('/signup', data=USER_DATA)
        data = USER_DATA.copy()
        data['password'] = 'different'
        response = self.app.post('/signup', data=data)
        self.assertEqual(response.status_code, codes.CONFLICT)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


class LoginTests(unittest.TestCase):
    """
    Tests for the user log in endpoint at ``/login``.
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        self.app.post('/signup', data=USER_DATA)

    def test_login(self):
        response = self.app.post('/login', data=USER_DATA)
        self.assertEqual(response.status_code, codes.OK)

    def test_login_non_existant(self):
        non_existant_user = {'email': 'fake@example.com', 'password': 'secret'}
        response = self.app.post('/login', data=non_existant_user)
        self.assertEqual(response.status_code, codes.NOT_FOUND)

    def test_login_wrong_password(self):
        data = USER_DATA.copy()
        data['password'] = 'incorrect'
        response = self.app.post('/login', data=data)
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
