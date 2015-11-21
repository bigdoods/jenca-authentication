from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

from requests import codes

db = SQLAlchemy()

class User(db.Model):
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

def create_app(database_uri):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app(database_uri='sqlite:////tmp/test.db')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    response_content = {'email': email, 'password': password}
    return jsonify(response_content), codes.OK

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']

    if User.query.filter_by(email=email).count():
        return jsonify({}), codes.CONFLICT

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    response_content = {'email': email, 'password': password}
    return jsonify(response_content), codes.CREATED

if __name__ == '__main__':
    # Specifying 0.0.0.0 as the host tells the operating system to listen on
    # all public IPs. This makes the server visible externally.
    # See http://flask.pocoo.org/docs/0.10/quickstart/#a-minimal-application
    app.run(host='0.0.0.0')
