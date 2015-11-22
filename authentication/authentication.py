import os

from flask import Flask, jsonify, request
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import (
    LoginManager, UserMixin, login_user, logout_user, login_required)
from flask.ext.sqlalchemy import SQLAlchemy

from requests import codes

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    A user has an email and password.
    """
    email = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)

    def get_id(self):
        """
        Return the email address to satify Flask-Login's requirements.
        """
        return self.email


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
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
app = create_app(database_uri=SQLALCHEMY_DATABASE_URI)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return
    None based on the userid.
    The userid was stored in the session environment by Flask-Login.
    user_loader stores the returned User object in current_user during every
    flask request.
    """
    return User.query.filter_by(email=userid).first()


@app.route('/login', methods=['POST'])
def login():
    """
    Login API endpoint.

    Return an OK status code and user details if a user with the given email
    and password exists, else give an appropriate error code.
    """
    email = request.form['email']
    password = request.form['password']

    existing_users = User.query.filter_by(email=email)
    if not existing_users.count():
        return jsonify({}), codes.NOT_FOUND

    user = existing_users.first()

    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({}), codes.UNAUTHORIZED

    login_user(user, remember=False)

    response_content = {'email': email, 'password': password}
    return jsonify(response_content), codes.OK


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Log the current user out.
    """
    logout_user()
    return jsonify({}), codes.OK


@app.route('/signup', methods=['POST'])
def signup():
    """
    Signup API endpoint.

    Return an OK status code and user details if a user with the given email
    and password does not exist, else give an appropriate error code.
    """
    email = request.form['email']
    password = request.form['password']

    if load_user(email) is not None:
        return jsonify({}), codes.CONFLICT

    password_hash = bcrypt.generate_password_hash(password)
    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    response_content = {'email': email, 'password': password}
    return jsonify(response_content), codes.CREATED

if __name__ == '__main__':   # pragma: no cover
    # Specifying 0.0.0.0 as the host tells the operating system to listen on
    # all public IPs. This makes the server visible externally.
    # See http://flask.pocoo.org/docs/0.10/quickstart/#a-minimal-application
    app.run(host='0.0.0.0')
