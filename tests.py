"""Tests for Chord Storm."""

import json
from unittest import TestCase
from server import app
from model import connect_to_db, db
from subproccess import call

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        call(['psql', 'testdb', '<', '/seed_data/test.sql'])

    def test_index(self):
        """Test index route."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Songs with only 3 chords', result.data)

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'test@test.com', 'password': 'test'},
                            follow_redirects=True
                            )
            self.assertEqual(session['user'], '1')
            self.assertIn("Favorites", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        call(['psql', 'testdb', '<', '/seed_data/test.sql'])

    def test_add_fav_json(self):
        """Test json route."""

        result = self.client.post("/songs/add_fav.json", data={'song_id': 365})
        response_dict = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(response_dict['success'])
        self.assertEqual(response_dict['song_id'], 365)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

if __name__ == '__main__':

    import unittest
    unittest.main()