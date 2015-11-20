from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/login', methods=['GET'])
def login():
    return jsonify({})


@app.route('/signup')
def signup():
    return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
