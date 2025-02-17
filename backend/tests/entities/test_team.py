from datetime import datetime
from unittest import TestCase

from entities.team import Team
from entities.player import Player

# @dataclass
# class Team:
#     id: int
#     name: str
#     coach: str
#     manager: str
#     league: str
#     players: List['Player'] = field(default_factory=list)  # Forward reference

class TestTeam(TestCase):
    def test_team(self):
        team = Team('team A', 'coach A', 'manager A', 'league A', [Player('player John', datetime(1985, 9, 22), datetime(2020, 9, 22))])
        self.assertEqual(team.id, None)
        self.assertEqual(team.name, 'team A')
        self.assertEqual(team.coach, 'coach A')
        self.assertEqual(team.manager, 'manager A')
        self.assertEqual(team.league, 'league A')
        self.assertEqual(team.players[0].id, None)
        self.assertEqual(team.players[0].name, 'player John')
        self.assertEqual(team.players[0].dob, datetime(1985, 9, 22))
        self.assertEqual(team.players[0].joined_group_date, datetime(2020, 9, 22))
