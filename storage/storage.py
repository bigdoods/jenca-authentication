"""
An authentication service for use in a Jenca Cloud.
"""

import os

from flask import Flask, jsonify, request
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

from flask.ext.sqlalchemy import SQLAlchemy
from flask_jsonschema import JsonSchema, ValidationError
from flask_negotiate import consumes

from requests import codes

db = SQLAlchemy()


class User(db.Model):
    """
    A user has an email and password.
    """
    email = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)


def create_app(database_uri):
    """
    Create an application with a database in a given location.

    :param database_uri: The location of the database for the application.
    :type database_uri: string
    :return: An application instance.
    :rtype: ``Flask``
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                         'sqlite:///:memory:')
app = create_app(database_uri=SQLALCHEMY_DATABASE_URI)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Inputs can be validated using JSON schema.
# Schemas are in app.config['JSONSCHEMA_DIR'].
# See https://github.com/mattupstate/flask-jsonschema for details.
app.config['JSONSCHEMA_DIR'] = os.path.join(app.root_path, 'schemas')
jsonschema = JsonSchema(app)


@login_manager.user_loader
def load_user_from_id(user_id):
    """
    Flask-Login ``user_loader`` callback.

    The ``user_id`` was stored in the session environment by Flask-Login.
    user_loader stores the returned ``User`` object in ``current_user`` during
    every flask request.

    See https://flask-login.readthedocs.org/en/latest/#flask.ext.login.LoginManager.user_loader.  # noqa

    :param user_id: The ID of the user Flask is trying to load.
    :type user_id: string
    :return: The user which has the email address ``user_id`` or ``None`` if
        there is no such user.
    :rtype: ``User`` or ``None``.
    """
    return User.query.filter_by(email=user_id).first()


@login_manager.token_loader
def load_user_from_token(auth_token):
    """
    Flask-Login token-loader callback.

    See https://flask-login.readthedocs.org/en/latest/#flask.ext.login.LoginManager.token_loader  # noqa

    :param auth_token: The authentication token of the user Flask is trying to
        load.
    :type user_id: string
    :return: The user which has the given authentication token or ``None`` if
        there is no such user.
    :rtype: ``User`` or ``None``.
    """
    for user in User.query.all():
        if user.get_auth_token() == auth_token:
            return user


@app.errorhandler(ValidationError)
def on_validation_error(error):
    """
    :resjson string title: An explanation that there was a validation error.
    :resjson string message: The precise validation error.
    :status 400:
    """
    return jsonify(
        title='There was an error validating the given arguments.',
        # By default on Python 2 errors will look like:
        # "u'password' is a required property".
        # This removes all "u'"s, and so could be dangerous.
        detail=error.message.replace("u'", "'"),
    ), codes.BAD_REQUEST


@app.route('/user/create', methods=['POST'])
@consumes('application/json')
@jsonschema.validate('user', 'create')
def signup():
    """
    Sign up a new user.

    :param email: The email address of the new user.
    :type email: string
    :param password_hash: A password hash to associate with the given ``email``
        address.
    :type password: string
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resjson string email: The email address of the new user.
    :resjson string password_hash: The password of the new user.
    :status 200: A user with the given ``email`` and ``password`` has been
        created.
    :status 409: There already exists a user with the given ``email``.
    """
    email = request.json['email']
    password_hash = request.json['password_hash']

    if load_user_from_id(email) is not None:
        return jsonify(
            title='There is already a user with the given email address.',
            detail='A user already exists with the email "{email}"'.format(
                email=email),
        ), codes.CONFLICT

    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify(email=email, password=password_hash), codes.CREATED

if __name__ == '__main__':   # pragma: no cover
    # Specifying 0.0.0.0 as the host tells the operating system to listen on
    # all public IPs. This makes the server visible externally.
    # See http://flask.pocoo.org/docs/0.10/quickstart/#a-minimal-application
    app.run(host='0.0.0.0', port=5001)
