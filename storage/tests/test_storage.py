"""
Tests for storage service.
"""

# TODO tests for getting all users
# TODO update the docs
# TODO Put the docs for this API in the docs
# TODO move things around so that all of the source is in one place (maybe
# with a `common` package)
# TODO Verified? Fake for this for the authentication tests

import json
import unittest

from flask.ext.sqlalchemy import orm
from requests import codes

from storage.storage import app as storage_app, db, User

USER_DATA = {'email': 'alice@example.com', 'password_hash': '123abc'}


class DatabaseTestCase(unittest.TestCase):
    """
    Set up and tear down an application with an in memory database for testing.
    """

    def setUp(self):
        storage_app.config['TESTING'] = True
        storage_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.storage_app = storage_app.test_client()
        self.storage_url_map = storage_app.url_map

        with storage_app.app_context():
            db.create_all()

    def tearDown(self):
        with storage_app.app_context():
            db.session.remove()
            db.drop_all()


class CreateUserTests(DatabaseTestCase):
    """
    Tests for the user creation endpoint at ``POST /users``.
    """

    def test_success_response(self):
        """
        A ``POST /users`` request with an email address and password hash
        returns a JSON response with user details and a CREATED status.
        """
        response = self.storage_app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)
        self.assertEqual(json.loads(response.data.decode('utf8')), USER_DATA)

    def test_missing_email(self):
        """
        A ``POST /users`` request without an email address returns a
        BAD_REQUEST status code and an error message.
        """
        data = USER_DATA.copy()
        data.pop('email')

        response = self.storage_app.post(
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
        A ``POST /users`` request without a password hash returns a BAD_REQUEST
        status code and an error message.
        """
        data = USER_DATA.copy()
        data.pop('password_hash')

        response = self.storage_app.post(
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
        A ``POST /users`` request for an email address which already exists
        returns a CONFLICT status code and error details.
        """
        self.storage_app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        data = USER_DATA.copy()
        data['password'] = 'different'
        response = self.storage_app.post(
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
        response = self.storage_app.post('/users', content_type='text/html')
        self.assertEqual(response.status_code, codes.UNSUPPORTED_MEDIA_TYPE)


class GetUserTests(DatabaseTestCase):
    """
    Tests for getting a user at ``GET /users/{email}``.
    """

    def test_success(self):
        """
        A ``GET`` request for an existing user an OK status code and the user's
        details.
        """
        self.storage_app.post(
            '/users',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        response = self.storage_app.get(
            '/users/{email}'.format(email=USER_DATA['email']),
            content_type='application/json')
        self.assertEqual(response.status_code, codes.OK)
        self.assertEqual(json.loads(response.data.decode('utf8')), USER_DATA)

    def test_non_existant_user(self):
        """
        A ``GET`` request for a user which does not exist returns a NOT_FOUND
        status code and error details.
        """
        response = self.storage_app.get(
            '/users/{email}'.format(email=USER_DATA['email']),
            content_type='application/json')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.NOT_FOUND)
        expected = {
            'title': 'The requested user does not exist.',
            'detail': 'No user exists with the email "{email}"'.format(
                email=USER_DATA['email']),
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)


class UserTests(DatabaseTestCase):
    """
    Tests for the ``User`` model.
    """

    def test_email_unique(self):
        """
        There cannot be two users with the same email address.
        """
        user_1 = User(email='email', password_hash='password_hash')
        user_2 = User(email='email', password_hash='different_hash')
        with storage_app.app_context():
            db.session.add(user_1)
            db.session.commit()
            db.session.add(user_2)
            with self.assertRaises(orm.exc.FlushError):
                db.session.commit()
