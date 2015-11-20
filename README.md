# jenca-authentication

Authentication service for Jenca Cloud
Python service with login and signup

Uses Flask

Build Docker image:

docker build -t jenca/authentication .
docker run --name jenca_authentication -p 5000:5000 -i -t jenca/authentication

Current commands:
login
signup

TODO:
* Make signup save a user to a database
* Tests
* Docker compose yml file
* Travis CI
* https://requires.io
* Flake8

In the future this might hold other user details
