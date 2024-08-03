import unittest
import json
from flask import Flask
from app import app  # Ensure this import is correct

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_move(self):
        response = self.app.post('/get_move', data=json.dumps({
            'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        }), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('move', data)

    def test_make_move(self):
        response = self.app.post('/make_move', data=json.dumps({
            'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
            'move': 'e2e4'
        }), content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('fen', data)
        self.assertIn('game_over', data)

if __name__ == '__main__':
    unittest.main()
