from unittest import TestCase
from datetime import datetime

from entities.player import Player

# @dataclass
# class Player:
#     id: Optional[int] = field(default=None, init=False)  # Optional and auto-generated if not provided
#     name: str
#     dob: datetime
#     joined_group_date: datetime

class TestPlayer(TestCase):
    def test_player(self):
        player = Player(name='player John', dob=datetime(1985, 9, 22), joined_group_date=datetime(2020, 9, 22))
        self.assertEqual(player.id, None)
        self.assertEqual(player.name, 'player John')
        self.assertEqual(player.dob, datetime(1985, 9, 22))
        self.assertEqual(player.joined_group_date, datetime(2020, 9, 22))
