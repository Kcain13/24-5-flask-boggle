from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        '''stuff to do before every test'''

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        '''make sure information is in the session and HTML is displayed'''

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.asseertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        '''test if word is valid by modifying the board in session'''

        with self.client as client:
            with client.session_transaction() as sees:
                sees['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-wrod?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        '''Test if word is in the dictionary'''

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        '''test if word is on the board'''

        self.client.get('/')
        response = self.client.get(
            '/check_word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')
