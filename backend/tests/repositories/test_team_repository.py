from unittest import TestCase

from entities.team import Team
from repositories.team_repository import TeamRepository


class TestTeamRepository(TestCase):
    def setUp(self):
        self.repository = TeamRepository()

    def test_add_team(self):
        self.repository.add(Team(name='Team 1', coach='Coach 1', manager='Manager 1', league='League 1', players=['Player 1', 'Player 2', 'Player 3']))
        self.assertEqual(len(self.repository.teams), 1)

    def test_get_team(self):
        team = Team(name='Team 1', coach='Coach 1', manager='Manager 1', league='League 1', players=['Player 1', 'Player 2', 'Player 3'])
        self.repository.add(team)
        self.assertEqual(self.repository.get(1), team)

    def test_get_team_by_name(self):
        team1 = Team(name='Team 1', coach='Coach 1', manager='Manager 1', league='League 1', players=['Player 1', 'Player 2', 'Player 3'])
        team2 = Team(name='Team 2', coach='Coach 2', manager='Manager 2', league='League 2', players=['Player 4', 'Player 5', 'Player 6'])
        self.repository.add(team1)
        self.repository.add(team2)
        self.assertEqual(self.repository.get_by_name('Team 1'), team1)
        self.assertEqual(self.repository.get_by_name('Team 2'), team2)

    def test_get_team_by_name_not_found(self):
        self.assertIsNone(self.repository.get_by_name('Team 1'))
        

    def test_update_team(self):
        team = Team(name='Team 1', coach='Coach 1', manager='Manager 1', league='League 1', players=['Player 1', 'Player 2', 'Player 3'])
        self.repository.add(team)
        team.name = 'Team 2'
        self.repository.update(team)
        self.assertEqual(self.repository.get(1).name, 'Team 2')

    def test_delete_team(self):
        team1 = Team(name='Team 1', coach='Coach 1', manager='Manager 1', league='League 1', players=['Player 1', 'Player 2', 'Player 3'])
        team2 = Team(name='Team 2', coach='Coach 2', manager='Manager 2', league='League 2', players=['Player 4', 'Player 5', 'Player 6'])
        team3 = Team(name='Team 3', coach='Coach 3', manager='Manager 3', league='League 3', players=['Player 7', 'Player 8', 'Player 9'])
        self.repository.add(team1)
        self.repository.add(team2)
        self.repository.add(team3)
        self.repository.delete(1)
        self.assertEqual(len(self.repository.teams), 2)
        self.assertEqual(self.repository.get(2), team2)
        self.assertEqual(self.repository.get(3), team3)

    def test_list_all_teams(self):
        self.repository.add(Team(name='Team 2', coach='Coach 2', manager='Manager 2', league='League 2', players=['Player 4', 'Player 5', 'Player 6']))
        self.repository.add(Team(name='Team 3', coach='Coach 3', manager='Manager 3', league='League 3', players=['Player 7', 'Player 8', 'Player 9']))
        self.assertEqual(len(self.repository.list_all()), 2)
