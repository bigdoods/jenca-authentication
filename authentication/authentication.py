from flask import Flask, jsonify, request
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app(database_uri='sqlite:////tmp/authentication.db')
bcrypt = Bcrypt(app)


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

    password_hash = existing_users.first().password_hash
    if not bcrypt.check_password_hash(password_hash, password):
        return jsonify({}), codes.UNAUTHORIZED

    response_content = {'email': email, 'password': password}
    return jsonify(response_content), codes.OK


@app.route('/signup', methods=['POST'])
def signup():
    """
    Signup API endpoint.

    Return an OK status code and user details if a user with the given email
    and password does not exist, else give an appropriate error code.
    """
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(email=email).count():
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
