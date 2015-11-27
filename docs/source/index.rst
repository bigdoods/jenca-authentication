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
   >>> url = authentication_url + '/signup'
   >>> headers = {'Content-Type': 'application/json'}
   >>> data = {"email": "jenca@example.com", "password": "secret"}
   >>> requests.post(url=url, headers=headers, data=json.dumps(data))
   <Response[201]>

.. testcleanup::

   >>> url = authentication_url + '/delete/' + data['email']
   >>> requests.delete()
