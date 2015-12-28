.PHONY: images test

VERSION = 1.0.0

# build the docker images
# the dev version includes development modules for running tests
images:
	docker build -t jenca-cloud/jenca-authentication:latest .
	docker build -f Dockerfile.dev -t jenca-cloud/jenca-authentication:latest-dev .
	docker rmi jenca-cloud/jenca-authentication:$(VERSION) jenca-cloud/jenca-authentication:$(VERSION)-dev
	docker tag jenca-cloud/jenca-authentication:latest jenca-cloud/jenca-authentication:$(VERSION)
	docker tag jenca-cloud/jenca-authentication:latest-dev jenca-cloud/jenca-authentication:$(VERSION)-dev

test:
	echo "need to work out how to run the tests"