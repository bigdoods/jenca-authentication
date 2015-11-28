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
requests.

First, set a variable for the IP address of the Docker host machine.

..    >>> docker_ip = subprocess.check_output(['docker-machine', 'ip',
.. 'dev']).strip()

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
   >>> data = json.dumps({"email": "jenca@example.com", "password": "secret"})
   >>> response = requests.post(url=signup_url, headers=headers, data=data)
   >>> response
   <Response [201]>
   >>> json.loads(response.text)
   {'email': 'jenca@example.com', 'password': 'secret'}
   >>> status_url = authentication_url + '/status'
   >>> status = requests.get(url=status_url, headers=headers)
   >>> status
   <Response [200]>
   >>> json.loads(status.text)
   {'is_authenticated': False}

.. TODO move this to just after we have "data" set

.. testcleanup::

   url = authentication_url + '/users/' + data['email']
   requests.delete(url, headers=headers)
