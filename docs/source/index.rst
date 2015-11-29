Jenca Authentication
====================

Authentication Service API Endpoints
------------------------------------

.. autoflask:: authentication.authentication:app
   :undoc-static:

Storage Service API Endpoints
-----------------------------

.. autoflask:: storage.storage:app
   :undoc-static:

Example Use
===========

It is possible to interact with the authentication service using Python's
``requests``.
It is also possible to connect to the service with other tools,
such as other programming languages or ``curl`` but this example shows use with Python.

.. TODO don't render the sleep
.. TODO disable CircleCI and Codeship
.. TODO Fix tests
.. TODO use Sphinx make
.. TODO set up the env variable in setup and use it in the tests
.. TODO Try running the unit tests without the mock responses when Docker is up

Prerequisites
-------------

Docker must be installed and running.
If Docker is running then ``docker ps`` will show a list of containers.
This list may be empty.

.. code-block:: bash

   $ docker ps
   CONTAINER ID   IMAGE   COMMAND  CREATED   STATUS   PORTS   NAMES

Install the Python dependencies for connecting to the Docker container.
It is best to do this within a virtualenv:

.. code-block:: bash

   (my_venvenv)$ pip install requests docker-compose

Getting Started
---------------

Set a variable for the IP address of the Docker host machine.
On Linux, usually the Docker host is ``0.0.0.0``:

.. code-block:: bash

   (my_venvenv) alice@linux$ DOCKER_HOST=0.0.0.0

On OS X and Windows, Docker is usually running in a virtual machine via Docker Machine:

.. code-block:: bash

   (my_venvenv) alice@osx$ docker-machine ls
   NAME   ACTIVE   DRIVER       STATE     URL                         SWARM
   dev    *        virtualbox   Running   tcp://192.168.99.100:2376
   (my_venvenv) alice@osx$ DOCKER_HOST=`docker-machine ip dev`

Start the containers for the microservices:

.. code-block:: bash

   (my_venvenv)$ docker-compose up -d

.. code-block:: python

   $ python
   >>>

Start a Python shell:

.. code-block:: python

   $ python
   >>>

.. doctest::

   >>> import subprocess
   >>> import json
   >>> import requests
   >>> subprocess.check_call(['docker-compose', 'build'])
   0
   >>> subprocess.check_call(['docker-compose', 'up', '-d'])
   0
   >>> docker_ip = b'0.0.0.0'
   >>> authentication_url = 'http://' + docker_ip.decode('utf8') + ':5000'
   >>> signup_url = authentication_url + '/signup'
   >>> headers = {'Content-Type': 'application/json'}
   >>> data = {"email": "jenca@example.com", "password": "secret"}
   >>> import time; time.sleep(5);
   >>> response = requests.post(url=signup_url, headers=headers, data=json.dumps(data))
   >>> response
   <Response [201]>
   >>> response.text
   "{'email': 'jenca@example.com', 'password': 'secret'}"
   >>> status_url = authentication_url + '/status'
   >>> status = requests.get(url=status_url, headers=headers)
   >>> status
   <Response [200]>
   >>> status.text
   "{'is_authenticated': False}"

.. TODO move this to just after we have "data" set

.. testcleanup::

   url = authentication_url + '/users/' + data['email']
   requests.delete(url, headers=headers)
