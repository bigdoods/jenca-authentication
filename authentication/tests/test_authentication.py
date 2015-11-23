import json
import unittest

from requests import codes
from werkzeug.http import parse_cookie

from authentication.authentication import app, db, User, bcrypt

USER_DATA = {'email': 'alice@example.com', 'password': 'secret'}


class APITestCase(unittest.TestCase):
    """
    Set up and tear down an application with an in memory database for testing.
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


class SignupTests(APITestCase):
    """
    Tests for the user sign up endpoint at ``/signup``.
    """

    def test_signup(self):
        """
        A signup ``POST`` request with an email address and password returns a
        JSON response with user credentials and a CREATED status.
        """
        response = self.app.post('/signup', data=USER_DATA)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)
        self.assertEqual(json.loads(response.data.decode('utf8')), USER_DATA)

    def test_passwords_hashed(self):
        """
        Passwords are hashed before being saved to the database.
        """
        self.app.post('/signup', data=USER_DATA)
        with app.app_context():
            user = User.query.filter_by(email=USER_DATA['email']).first()
        self.assertTrue(bcrypt.check_password_hash(user.password_hash,
                                                   USER_DATA['password']))

    def test_missing_data(self):
        """
        A signup request without an email address or password returns a
        BAD_REQUEST status code.
        """
        response = self.app.post('/signup', data={})
        self.assertEqual(response.status_code, codes.BAD_REQUEST)

    def test_existing_user(self):
        """
        A signup request for an email address which already exists returns a
        CONFLICT status code.
        """
        self.app.post('/signup', data=USER_DATA)
        data = USER_DATA.copy()
        data['password'] = 'different'
        response = self.app.post('/signup', data=data)
        self.assertEqual(response.status_code, codes.CONFLICT)


class LoginTests(APITestCase):
    """
    Tests for the user log in endpoint at ``/login``.
    """

    def test_login(self):
        """
        Logging in as a user which has been signed up returns an OK status
        code.
        """
        self.app.post('/signup', data=USER_DATA)
        response = self.app.post('/login', data=USER_DATA)
        self.assertEqual(response.status_code, codes.OK)

    def test_login_non_existant(self):
        """
        Attempting to log in as a user which has been not been signed up
        returns a NOT_FOUND status code.
        """
        response = self.app.post('/login', data=USER_DATA)
        self.assertEqual(response.status_code, codes.NOT_FOUND)

    def test_login_wrong_password(self):
        """
        Attempting to log in with an incorrect password returns an UNAUTHORIZED
        status code.
        """
        self.app.post('/signup', data=USER_DATA)
        data = USER_DATA.copy()
        data['password'] = 'incorrect'
        response = self.app.post('/login', data=data)
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)

    def test_remember_me_cookie_set(self):
        """
        A "Remember Me" token is in the response header of a successful login.
        """
        self.app.post('/signup', data=USER_DATA)
        response = self.app.post('/login', data=USER_DATA)
        cookies = response.headers.getlist('Set-Cookie')

        items = [list(parse_cookie(cookie).items())[0] for cookie in cookies]
        headers_dict = {key: value for key, value in items}
        email, user_id = headers_dict['remember_token'].split('|')
        self.assertEqual(email, USER_DATA['email'])


class LogoutTests(APITestCase):
    """
    Tests for the user log out endpoint at ``/logout``.
    """

    def test_logout(self):
        """
        A POST request to log out when a user is logged in returns an OK status
        code.
        """
        self.app.post('/signup', data=USER_DATA)
        self.app.post('/login', data=USER_DATA)
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, codes.OK)

    def test_not_logged_in(self):
        """
        A POST request to log out when no user is logged in returns an
        UNAUTHORIZED status code.
        """
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)

    def test_logout_twice(self):
        """
        A POST request to log out, after a successful log out attempt returns
        an UNAUTHORIZED status code.
        """
        self.app.post('/signup', data=USER_DATA)
        self.app.post('/login', data=USER_DATA)
        self.app.post('/logout')
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)