[![Requirements Status](https://requires.io/github/jenca-cloud/jenca-authentication/requirements.svg?branch=master)](https://requires.io/github/jenca-cloud/jenca-authentication/requirements/?branch=master)

# jenca-authentication

Authentication service for Jenca Cloud
Python service with login and signup

## Development

The requirements for running this are:
* Docker (with docker-machine and docker-compose) (probably you can use the Jenca Cloud Vagrant development environment)

For development you need Python and to install the requirements

Uses Flask http://flask.pocoo.org

Start the API service:

```
docker-compose build
docker-compose up
```

On OS X with Docker machine I've been running:

```
$ docker-machine ip dev
$ 192.168.99.100
$ curl 192.168.99.100:5000/login
```

for example

Current commands:
login
signup

## TODO

* Make signup save a user to a database (Flask-SQLAlchemy) - maybe https://flask-login.readthedocs.org/en/latest/
* Tests
* Travis CI (tox?)
* https://requires.io
* Flake8
* Automate API docs (maybe use a schema, sphinx)
* name > email
* hash passwords (Flask-Bcrypt)

In the future this might hold other user details
