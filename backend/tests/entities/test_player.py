from unittest import TestCase
from datetime import datetime

from entities.player import Player

# @dataclass
# class Player:
#     id: int
#     name: str
#     dob: str
#     age: int # derived from dob
#     joined_group_date: str
#     no_of_sessions: int  # number of sessions available

class TestPlayer(TestCase):
    def test_player(self):
        player = Player(1, 'player John', datetime(1985, 9, 22), '0', datetime(2020, 9, 22))
        self.assertEqual(player.id, 1)
        self.assertEqual(player.name, 'player John')
        self.assertEqual(player.dob, datetime(1985, 9, 22))
        self.assertEqual(player.age, 39)
        self.assertEqual(player.joined_group_date, datetime(2020, 9, 22))
