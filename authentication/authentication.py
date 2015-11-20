from flask import Flask
app = Flask(__name__)

@app.route('/login')
def api_articles():
    return 'logged in'

@app.route('/signup')
def api_article():
    return 'signed up'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
