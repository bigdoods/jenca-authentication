[![Requirements Status](https://requires.io/github/jenca-cloud/jenca-authentication/requirements.svg?branch=master)](https://requires.io/github/jenca-cloud/jenca-authentication/requirements/?branch=master) [![Build Status](https://travis-ci.org/jenca-cloud/jenca-authentication.svg?branch=master)](https://travis-ci.org/jenca-cloud/jenca-authentication) [![Coverage Status](https://coveralls.io/repos/jenca-cloud/jenca-authentication/badge.svg?branch=master&service=github)](https://coveralls.io/github/jenca-cloud/jenca-authentication?branch=master)

# jenca-authentication

An authentication service for Jenca Cloud.

## API

* `/login` takes `email` and `password`.
* `/signup` takes `email` and `password`.
* `/logout`.


## Running this service

This comes with a [Docker Compose](https://docs.docker.com/compose/) file. 

With Docker Compose available, perhaps in the Jenca Cloud Vagrant development environment, run:

```
docker-compose build
docker-compose up
```

to start the API service.

To run commands against the API, n OS X with Docker Machine for example:

```
$ docker-machine ip dev
$ 192.168.99.100
$ curl -X POST \
  -g '192.168.99.100:5000/signup' \
  -d email='user@example.com' \
  -d password='secret' \
  -c ~/Desktop/my_cookie
```

## Development

This service is written using Python and [Flask](http://flask.pocoo.org).

To start developing quickly, it is recommended that you create a `virtualenv` and install the requirements and run the tests as is done in `.travis.yml`.

Tests are run on [Travis-CI](https://travis-ci.org/jenca-cloud/jenca-authentication).

## TODO

* Better persistence of the database with Docker volumes.
* Better auth tokens, see https://flask-login.readthedocs.org/en/latest/#remember-me.
* Perhaps login should happen after signup, this should be factored out.
* API responses should have good messages, data, not just status codes
* Automated, good API docs (instead of this terrible README solution) probably sphinxcontrib.autohttp.flask
* Validate schema of JSON, e.g. with https://github.com/mattupstate/flask-jsonschema or http://pythonhosted.org/Flask-Inputs/
