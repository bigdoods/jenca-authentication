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

.. TODO: Get Travis to run this
.. TODO support different docker hosts, probably with a test setup

.. doctest::

   >>> import subprocess
   >>> import json
   >>> import requests
   >>> subprocess.check_call(['docker-compose', 'build'])
   0
   >>> subprocess.check_call(['docker-compose', 'up', '-d'])
   0
   >>> docker_ip = subprocess.check_output(['docker-machine', 'ip', 'dev']).strip()
   >>> authentication_url = 'http://' + docker_ip.decode('utf8') + ':5000'
   >>> signup_url = authentication_url + '/signup'
   >>> headers = {'Content-Type': 'application/json'}
   >>> data = {"email": "jenca@example.com", "password": "secret"}
   >>> response = requests.post(url=signup_url, headers=headers, data=json.dumps(data))
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
   >>> import pdb; pdb.set_trace()

.. testcleanup::

   url = authentication_url + '/users/' + data['email']
   requests.delete(url, headers=headers)
