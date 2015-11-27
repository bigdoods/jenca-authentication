"""
Test tools for the storage service.
"""

import unittest

from storage.storage import app, db


class InMemoryStorageTests(unittest.TestCase):
    """
    Set up and tear down an application with an in memory database for testing.
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.storage_app = app.test_client()
        self.storage_url_map = app.url_map

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
