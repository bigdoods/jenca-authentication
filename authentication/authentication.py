from flask import Flask, jsonify, request
from requests import codes

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password']
    response_content = {'email': username, 'password': password}
    return jsonify(response_content), codes.OK

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['email']
    password = request.form['password']
    response_content = {'email': username, 'password': password}
    return jsonify(response_content), codes.CREATED

if __name__ == '__main__':
    # Specifying 0.0.0.0 as the host tells the operating system to listen on
    # all public IPs. This makes the server visible externally.
    # See http://flask.pocoo.org/docs/0.10/quickstart/#a-minimal-application
    app.run(host='0.0.0.0', debug=True)
