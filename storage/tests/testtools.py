"""
Test tools for the storage service.
"""

import unittest

from storage.storage import app as storage_app, db


class InMemoryStorageTests(unittest.TestCase):
    """
    Set up and tear down an application with an in memory database for testing.
    """

    def setUp(self):
        storage_app.config['TESTING'] = True
        storage_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.storage_app = storage_app.test_client()
        self.storage_url_map = storage_app.url_map

        with storage_app.app_context():
            db.create_all()

    def tearDown(self):
        with storage_app.app_context():
            db.session.remove()
            db.drop_all()
