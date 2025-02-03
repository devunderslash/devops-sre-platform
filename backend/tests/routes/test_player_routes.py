from unittest import TestCase
from unittest.mock import patch
from app import app
from flask import Flask
from routes.player_routes import player_bp

from datetime import datetime
import logging

class TestPlayerRoutes(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(player_bp, url_prefix='/api', name='test_player_bp')
        self.client = self.app.test_client()

    @patch('routes.player_routes.player_service')
    def test_add_player_returns_201(self, mock_player_service):
        mock_player_service.add_player.return_value = None
        response = self.client.post('/api/players', json={'id': 1, 'name': 'John Doe', 'dob': '1985-09-22', 'joined_group_date': '2020-09-22'})
        self.assertEqual(response.status_code, 201)

    @patch('routes.player_routes.player_service')
    def test_add_player_returns_400_with_invalid_data_passed(self, mock_player_service):
        mock_player_service.add_player.return_value = None
        response = self.client.post('/api/players', json={'id': 'blue', 'name': 'John Doe', 'dob': '1985-09-22', 'joined_group_date': '2020-09-22'})
        self.assertEqual(response.status_code, 400)