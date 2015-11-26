"""
Tests for storage service.
"""

# TODO Replace tests here with just tests for the new API
# TODO Put the docs for this API in the docs
# TODO move things around so that all of the source is in one place (maybe
# with a `common` package)
# TODO change Travis to run these tests too
# TODO Verified? Fake for this for the authentication tests
# TODO rip some tests out of authentication

import json
import unittest

from requests import codes

from authentication.authentication import app, db

USER_DATA = {'email': 'alice@example.com', 'password_hash': '123abc'}


class DatabaseTestCase(unittest.TestCase):
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


class CreateUserTests(DatabaseTestCase):
    """
    Tests for the user creation endpoint at ``POST /users``.
    """

    def test_create_user(self):
        """
        A signup ``POST`` request with an email address and password hash
        returns a JSON response with user details and a CREATED status.
        """
        response = self.app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)
        self.assertEqual(json.loads(response.data.decode('utf8')), USER_DATA)

    def test_missing_email(self):
        """
        A signup request without an email address returns a BAD_REQUEST status
        code and an error message.
        """
        data = USER_DATA.copy()
        data.pop('email')

        response = self.app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(data))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.BAD_REQUEST)
        expected = {
            'title': 'There was an error validating the given arguments.',
            'detail': "'email' is a required property",
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_missing_password_hash(self):
        """
        A signup request without a password hash returns a BAD_REQUEST status
        code and an error message.
        """
        data = USER_DATA.copy()
        data.pop('password_hash')

        response = self.app.post(
            '/users',
            content_type='application/json',
            data=json.dumps({'email': USER_DATA['email']}))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.BAD_REQUEST)
        expected = {
            'title': 'There was an error validating the given arguments.',
            'detail': "'password_hash' is a required property",
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_existing_user(self):
        """
        A signup request for an email address which already exists returns a
        CONFLICT status code and error details.
        """
        self.app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        data = USER_DATA.copy()
        data['password'] = 'different'
        response = self.app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CONFLICT)
        expected = {
            'title': 'There is already a user with the given email address.',
            'detail': 'A user already exists with the email "{email}"'.format(
                email=USER_DATA['email']),
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_incorrect_content_type(self):
        """
        If a Content-Type header other than 'application/json' is given, an
        UNSUPPORTED_MEDIA_TYPE status code is given.
        """
        response = self.app.post('/users', content_type='text/html')
        self.assertEqual(response.status_code, codes.UNSUPPORTED_MEDIA_TYPE)


class GetUserTests(DatabaseTestCase):
    """
    Tests for getting a user at ``GET /users/{email}``.
    """

    def test_get_user(self):
        """
        TODO
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.assertEqual(response.status_code, codes.OK)

    def test_non_existant_user(self):
        """
        Attempting to log in as a user which has been not been signed up
        returns a NOT_FOUND status code and error details..
        """
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.NOT_FOUND)
        expected = {
            'title': 'The requested user does not exist.',
            'detail': 'No user exists with the email "{email}"'.format(
                email=USER_DATA['email']),
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_wrong_password(self):
        """
        Attempting to log in with an incorrect password returns an UNAUTHORIZED
        status code and error details.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        data = USER_DATA.copy()
        data['password'] = 'incorrect'
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(data))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
        expected = {
            'title': 'An incorrect password was provided.',
            'detail': 'The password for the user "{email}" does not match the '
                      'password provided.'.format(email=USER_DATA['email']),
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_missing_email(self):
        """
        A login request without an email address returns a BAD_REQUEST status
        code and an error message.
        """
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps({'password': USER_DATA['password']}))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.BAD_REQUEST)
        expected = {
            'title': 'There was an error validating the given arguments.',
            'detail': "'email' is a required property",
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_missing_password(self):
        """
        A login request without a password returns a BAD_REQUEST status code
        and an error message.
        """
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps({'email': USER_DATA['email']}))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.BAD_REQUEST)
        expected = {
            'title': 'There was an error validating the given arguments.',
            'detail': "'password' is a required property",
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_incorrect_content_type(self):
        """
        If a Content-Type header other than 'application/json' is given, an
        UNSUPPORTED_MEDIA_TYPE status code is given.
        """
        response = self.app.post('/login', content_type='text/html')
        self.assertEqual(response.status_code, codes.UNSUPPORTED_MEDIA_TYPE)
