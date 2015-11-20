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

* Make signup save a user to a database
* Tests
* Travis CI
* https://requires.io
* Flake8
* These should use proper HTTP request headers
* Automate API docs

In the future this might hold other user details
