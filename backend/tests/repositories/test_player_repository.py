from datetime import datetime
from unittest import TestCase

from entities.player import Player
from repositories.player_repository import PlayerRepository


class TestPlayerRepository(TestCase):
    def setUp(self):
        self.repository = PlayerRepository()

    def test_add_player(self):
        self.repository.add(Player(1, 'John Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22)))
        self.assertEqual(len(self.repository.players), 1)

    def test_get_player(self):
        player = Player(1, 'John Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        self.repository.add(player)
        self.assertEqual(self.repository.get(1), player)

    def test_get_player_by_name(self):
        player1 = Player(1, 'John Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        player2 = Player(2, 'Jane Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        self.repository.add(player1)
        self.repository.add(player2)

        self.assertEqual(self.repository.get_by_name('John Doe'), player1)
        self.assertEqual(self.repository.get_by_name('Jane Doe'), player2)

    def test_update_player(self):
        player = Player(1, 'John Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        self.repository.add(player)
        player.name = 'Jane Doe'
        self.repository.update(player)
        self.assertEqual(self.repository.get(1).name, 'Jane Doe')

    def test_delete_player(self):
        player1 = Player(1, 'John Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        player2 = Player(2, 'Jane Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        self.repository.add(player1)
        self.repository.add(player2)
        self.repository.delete(1)

        self.assertEqual(len(self.repository.players), 1)
        self.assertEqual(self.repository.get(2), player2)

    def test_list_all_players(self):
        self.repository.add(Player(1, 'John Doe', datetime(1985, 9, 22), '0', datetime(2020, 9, 22)))
        self.repository.add(Player(2, 'Jane Done', datetime(1985, 9, 22), '0', datetime(2020, 9, 22)))
        self.assertEqual(len(self.repository.list_all()), 2)
