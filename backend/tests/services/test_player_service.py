from datetime import datetime 
from unittest import TestCase

from entities.player import Player
from repositories.player_repository import PlayerRepository
from services.player_service import PlayerService


class TestPlayerService(TestCase):
    def setUp(self):
        self.service = PlayerService(PlayerRepository())

    def test_add_player(self):
        self.service.add_player(Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.assertEqual(len(self.service.list_all_players()), 1)

    def test_get_player(self):
        player = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.service.add_player(player)
        self.assertEqual(self.service.get_player(1), player)

    def test_get_player_by_name(self):
        player1 = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        player2 = Player(name='Jane Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.service.add_player(player1)
        self.service.add_player(player2)

        self.assertEqual(self.service.get_player_by_name('John Doe'), player1)
        self.assertEqual(self.service.get_player_by_name('Jane Doe'), player2)

    def test_get_player_by_name_not_found(self):
        self.assertIsNone(self.service.get_player_by_name('John Doe'))
        
    def test_update_player(self):
        player = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.service.add_player(player)
        player.name = 'Jane Doe'
        self.service.update_player(player)
        self.assertEqual(self.service.get_player(1).name, 'Jane Doe')

    def test_delete_player(self):
        player1 = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        player2 = Player(name='Jane Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.service.add_player(player1)
        self.service.add_player(player2)
        self.service.delete_player(1)

        self.assertEqual(len(self.service.list_all_players()), 1)
        self.assertEqual(self.service.get_player(2), player2)

    def test_list_all_players(self):
        self.service.add_player(Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.service.add_player(Player(name='Jane Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.assertEqual(len(self.service.list_all_players()), 2)

    def test_list_all_players_empty(self):
        self.assertEqual(len(self.service.list_all_players()), 0)

    def test_list_all_players_by_year_of_birth(self):
        self.service.add_player(Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.service.add_player(Player(name='Jane Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.service.add_player(Player(name='Jahn Dope', dob=datetime(1986, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        print(self.service.list_all_players_by_year_of_birth(1985))
        self.assertEqual(len(self.service.list_all_players_by_year_of_birth(1985)), 2)

