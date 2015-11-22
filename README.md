[![Requirements Status](https://requires.io/github/jenca-cloud/jenca-authentication/requirements.svg?branch=master)](https://requires.io/github/jenca-cloud/jenca-authentication/requirements/?branch=master)

[![Build Status](https://travis-ci.org/jenca-cloud/jenca-authentication.svg?branch=master)](https://travis-ci.org/jenca-cloud/jenca-authentication)

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

### Tests

Tests are run on [Travis-CI](https://travis-ci.org/jenca-cloud/jenca-authentication).
See `.travis.yml` for details on how the tests are run.

## TODO

* Use a login manager, maybe https://flask-login.readthedocs.org/en/latest/
* Automate API docs (maybe use a schema, sphinx)
* hash passwords (Flask-Bcrypt)
* Try a formatter (YAPF?)
* Lint markdown

In the future this might hold other user details
