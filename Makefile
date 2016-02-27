.PHONY: images test

VERSION = 1.0.0
SERVICE = jenca-authentication
HUBACCOUNT = jenca

# build the docker images
# the dev version includes development modules for running tests
images:
	docker build -t $(HUBACCOUNT)/$(SERVICE):latest .
	docker build -f Dockerfile.dev -t $(HUBACCOUNT)/$(SERVICE):latest-dev .
	docker rmi $(HUBACCOUNT)/$(SERVICE):$(VERSION) $(HUBACCOUNT)/$(SERVICE):$(VERSION)-dev || true
	docker tag $(HUBACCOUNT)/$(SERVICE):latest $(HUBACCOUNT)/$(SERVICE):$(VERSION)
	docker tag $(HUBACCOUNT)/$(SERVICE):latest-dev $(HUBACCOUNT)/$(SERVICE):$(VERSION)-dev

# run the tests inside a docker container
# it will auto-delete itself once complete
test:
	docker run -ti --rm \
		--entrypoint "coverage" \
		$(HUBACCOUNT)/$(SERVICE):latest-dev \
		run --source=authentication,storage -m unittest discover