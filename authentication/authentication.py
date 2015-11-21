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
    app.run(host='0.0.0.0')
