"""
Tests for authentication.authentication.
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

from flask.ext.login import make_secure_token
from flask.ext.sqlalchemy import orm
from requests import codes
from werkzeug.http import parse_cookie

from authentication.authentication import (
    app,
    bcrypt,
    db,
    load_user_from_id,
    load_user_from_token,
    User,
)

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
    Tests for the user sign up endpoint at ``POST /users``.
    """

    def test_signup(self):
        """
        A signup ``POST`` request with an email address and password returns a
        JSON response with user credentials and a CREATED status.
        """
        response = self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.CREATED)
        self.assertEqual(json.loads(response.data.decode('utf8')), USER_DATA)

    def test_passwords_hashed(self):
        """
        Passwords are hashed before being saved to the database.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        with app.app_context():
            user = User.query.filter_by(email=USER_DATA['email']).first()
        self.assertTrue(bcrypt.check_password_hash(user.password_hash,
                                                   USER_DATA['password']))

    def test_missing_email(self):
        """
        A signup request without an email address returns a BAD_REQUEST status
        code and an error message.
        """
        response = self.app.post(
            '/signup',
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
        A signup request without a password returns a BAD_REQUEST status code
        and an error message.
        """
        response = self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps({'email': USER_DATA['email']}))
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, codes.BAD_REQUEST)
        expected = {
            'title': 'There was an error validating the given arguments.',
            'detail': "'password' is a required property",
        }
        self.assertEqual(json.loads(response.data.decode('utf8')), expected)

    def test_existing_user(self):
        """
        A signup request for an email address which already exists returns a
        CONFLICT status code and error details.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        data = USER_DATA.copy()
        data['password'] = 'different'
        response = self.app.post(
            '/signup',
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
        response = self.app.post('/signup', content_type='text/html')
        self.assertEqual(response.status_code, codes.UNSUPPORTED_MEDIA_TYPE)


class LoginTests(DatabaseTestCase):
    """
    Tests for the user log in endpoint at ``/login``.
    """

    def test_login(self):
        """
        Logging in as a user which has been signed up returns an OK status
        code.
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

    def test_remember_me_cookie_set(self):
        """
        A "Remember Me" token is in the response header of a successful login
        with the value of ``User.get_auth_token`` for the logged in user.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        cookies = response.headers.getlist('Set-Cookie')

        items = [list(parse_cookie(cookie).items())[0] for cookie in cookies]
        headers_dict = {key: value for key, value in items}
        token = headers_dict['remember_token']
        with app.app_context():
            user = load_user_from_id(user_id=USER_DATA['email'])
            self.assertEqual(token, user.get_auth_token())

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


class LogoutTests(DatabaseTestCase):
    """
    Tests for the user log out endpoint at ``/logout``.
    """

    def test_logout(self):
        """
        A POST request to log out when a user is logged in returns an OK status
        code.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        response = self.app.post('/logout', content_type='application/json')
        self.assertEqual(response.status_code, codes.OK)

    def test_not_logged_in(self):
        """
        A POST request to log out when no user is logged in returns an
        UNAUTHORIZED status code.
        """
        response = self.app.post('/logout', content_type='application/json')
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)

    def test_logout_twice(self):
        """
        A POST request to log out, after a successful log out attempt returns
        an UNAUTHORIZED status code.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        self.app.post('/logout', content_type='application/json')
        response = self.app.post('/logout', content_type='application/json')
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)

    def test_incorrect_content_type(self):
        """
        If a Content-Type header other than 'application/json' is given, an
        UNSUPPORTED_MEDIA_TYPE status code is given.
        """
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, codes.UNSUPPORTED_MEDIA_TYPE)


class LoadUserTests(DatabaseTestCase):
    """
    Tests for ``load_user_from_id``, which is a function required by
    Flask-Login.
    """

    def test_user_exists(self):
        """
        If a user exists with the email given as the user ID to
        ``load_user_from_id``, that user is returned.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        with app.app_context():
            self.assertEqual(load_user_from_id(user_id=USER_DATA['email']),
                             User(email=USER_DATA['email']))

    def test_user_does_not_exist(self):
        """
        If no user exists with the email given as the user ID to
        ``load_user_from_id``, ``None`` is returned.
        """
        with app.app_context():
            self.assertIsNone(load_user_from_id(user_id='email'))


class LoadUserFromTokenTests(DatabaseTestCase):
    """
    Tests for ``load_user_from_token``, which is a function required by
    Flask-Login when using secure "Alternative Tokens".
    """

    def test_load_user_from_token(self):
        """
        A user is loaded if their token is provided to
        ``load_user_from_token``.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        cookies = response.headers.getlist('Set-Cookie')

        items = [list(parse_cookie(cookie).items())[0] for cookie in cookies]
        headers_dict = {key: value for key, value in items}
        token = headers_dict['remember_token']
        with app.app_context():
            user = load_user_from_id(user_id=USER_DATA['email'])
            self.assertEqual(load_user_from_token(auth_token=token), user)

    def test_fake_token(self):
        """
        If a token does not belong to a user, ``None`` is returned.
        """
        with app.app_context():
            self.assertIsNone(load_user_from_token(auth_token='fake_token'))

    def test_modified_password(self):
        """
        If a user's password (hash) is modified, their token is no longer
        valid.
        """
        self.app.post(
            '/signup',
            content_type='application/json',
            data=json.dumps(USER_DATA))
        response = self.app.post(
            '/login',
            content_type='application/json',
            data=json.dumps(USER_DATA))

        cookies = response.headers.getlist('Set-Cookie')

        items = [list(parse_cookie(cookie).items())[0] for cookie in cookies]
        headers_dict = {key: value for key, value in items}
        token = headers_dict['remember_token']
        with app.app_context():
            user = load_user_from_id(user_id=USER_DATA['email'])
            user.password_hash = 'new_hash'
            self.assertIsNone(load_user_from_token(auth_token=token))


class UserTests(DatabaseTestCase):
    """
    Tests for the ``User`` model.
    """

    def test_get_id(self):
        """
        ``User.get_id`` returns the email of a ``User``. This is required by
        Flask-Login as a unique identifier.
        """
        user = User(email='email', password_hash='password_hash')
        self.assertEqual(user.get_id(), 'email')

    def test_email_unique(self):
        """
        There cannot be two users with the same email address.
        """
        user_1 = User(email='email', password_hash='password_hash')
        user_2 = User(email='email', password_hash='different_hash')
        with app.app_context():
            db.session.add(user_1)
            db.session.commit()
            db.session.add(user_2)
            with self.assertRaises(orm.exc.FlushError):
                db.session.commit()

    def test_get_auth_token(self):
        """
        Authentication tokens are created using Flask-Login's
        ``make_secure_token`` function and the email address and password of
        the user.
        """
        user = User(email='email', password_hash='password_hash')
        with app.app_context():
            self.assertEqual(user.get_auth_token(),
                             make_secure_token('email', 'password_hash'))

    def test_different_password_different_token(self):
        """
        If a user has a different password hash, it will have a different
        token.
        """
        user_1 = User(email='email', password_hash='password_hash')
        user_2 = User(email='email', password_hash='different_hash')
        with app.app_context():
            self.assertNotEqual(user_1.get_auth_token(),
                                user_2.get_auth_token())
