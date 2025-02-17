from unittest import TestCase
from unittest.mock import patch
from app import app
from entities.player import Player
from flask import Flask
from routes.player_routes import player_bp


# import os

# set environment variable to testing
# os.environ['TESTING'] = 'True'

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
        response = self.client.post('/api/players', json={'id': 'blue', 'name': 3, 'dob': '1985-09-22', 'joined_group_date': '2020-09-22'})
        self.assertEqual(response.status_code, 400)

    @patch('routes.player_routes.player_service')
    def test_list_all_players_returns_200(self, mock_player_service):
        mock_player_service.list_all_players.return_value = []
        response = self.client.get('/api/players')
        self.assertEqual(response.status_code, 200)

    @patch('routes.player_routes.player_service')
    def test_get_player_returns_200(self, mock_player_service):
        mock_player_service.get_player.return_value = Player(id=1, name='John Doe', dob='1985-09-22', joined_group_date='2020-09-22')
        response = self.client.get('/api/players/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', response.get_data(as_text=True))

    @patch('routes.player_routes.player_service')
    def test_get_player_returns_404(self, mock_player_service):
        mock_player_service.get_player.return_value = None
        response = self.client.get('/api/players/1')
        self.assertEqual(response.status_code, 404)

    @patch('routes.player_routes.player_service')
    def test_get_player_by_name_returns_200(self, mock_player_service):
        mock_player_service.get_player_by_name.return_value = Player(id=1, name='John Doe', dob='1985-09-22', joined_group_date='2020-09-22')
        response = self.client.get('/api/players/John Doe')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', response.get_data(as_text=True))

    @patch('routes.player_routes.player_service')
    def test_get_player_by_name_returns_404(self, mock_player_service):
        mock_player_service.get_player_by_name.return_value = None
        response = self.client.get('/api/players/John Doe')
        self.assertEqual(response.status_code, 404)

    @patch('routes.player_routes.player_service')
    def test_update_player_returns_200(self, mock_player_service):
        mock_player_service.update_player.return_value = None
        response = self.client.put('/api/players/1', json={'id': 1, 'name': 'Jane Doe', 'dob': '1985-09-22', 'joined_group_date': '2020-09-22'})
        self.assertEqual(response.status_code, 200)

    # @patch('routes.player_routes.player_service')
    # def test_delete_player_returns_204(self, mock_player_service):
    #     mock_player_service.delete_player.return_value = None
    #     response = self.client.delete('/api/players/1')
    #     self.assertEqual(response.status_code, 204)
