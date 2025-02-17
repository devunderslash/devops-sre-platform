from datetime import datetime
from typing import Optional
from unittest import TestCase

from entities.player import Player
from repositories.player_repository import PlayerRepository
    

class TestPlayerRepository(TestCase):
    def setUp(self):
        self.repository = PlayerRepository()

    def test_with_player_repository_dictionary(self):
        repository = PlayerRepository()
        player = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        repository.add(player)
        self.assertEqual(len(repository.list_all()), 1)

    def test_add_player(self):
        player = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.repository.add(player)
        self.assertEqual(len(self.repository.players), 1)
        self.assertEqual(player.id, 1)

    def test_get_player(self):
        player = Player(name='John Does', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.repository.add(player)

        self.assertEqual(self.repository.get(1), player)
        # confirm that id has been generated
        self.assertEqual(self.repository.get(1).id, 1)

    def test_get_player_by_name(self):
        player1 = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        player2 = Player(name='Jane Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.repository.add(player1)
        self.repository.add(player2)

        self.assertEqual(self.repository.get_by_name('John Doe'), player1)
        self.assertEqual(self.repository.get_by_name('Jane Doe'), player2)

    def test_update_player(self):
        player = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.repository.add(player)
        player.name = 'Jane Doe'
        self.repository.update(player)
        print(self.repository.players)
        self.assertEqual(self.repository.get(1).name, 'Jane Doe')

    def test_delete_player(self):
        player1 = Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        player2 = Player(name='Jane Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.repository.add(player1)
        self.repository.add(player2)
        self.repository.delete(1)

        self.assertEqual(len(self.repository.players), 1)
        self.assertEqual(self.repository.players.get(2), player2)

    def test_list_all_players(self):
        self.repository.add(Player(name='John Doe', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.repository.add(Player(name='Jane Done', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22)))
        self.assertEqual(len(self.repository.list_all()), 2)
