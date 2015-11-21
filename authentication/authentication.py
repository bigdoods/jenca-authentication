from flask import Flask, jsonify, request
from flask.ext.login import UserMixin, LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from requests import codes

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy()
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# @login_manager.user_loader
# def user_loader(user_id):
#     """Given *user_id*, return the associated User object.
#
#     :param unicode user_id: user_id (email) user to retrieve
#     """
#     return User.query.get(user_id)

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
    user = User(email=email, password=password)
    import pdb; pdb.set_trace()
    db.session.add(user)
    db.session.commit()
    response_content = {'email': email, 'password': password}
    return jsonify(response_content), codes.CREATED

if __name__ == '__main__':
    # Specifying 0.0.0.0 as the host tells the operating system to listen on
    # all public IPs. This makes the server visible externally.
    # See http://flask.pocoo.org/docs/0.10/quickstart/#a-minimal-application
    app.run(host='0.0.0.0')
