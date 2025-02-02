from unittest import TestCase

from entities.team import Team
from services.team_service import TeamService


class TestTeamservice(TestCase):
    def setUp(self):
        self.service = TeamService()

    def test_add_team(self):
        self.service.add_team(Team(1, 'team A', 'coach A', 'manager A', 'league A'))
        self.assertEqual(len(self.service.list_all_teams()), 1)

    def test_get_team(self):
        team = Team(1, 'team A', 'coach A', 'manager A', 'league A')
        self.service.add_team(team)
        self.assertEqual(self.service.get_team(1), team)

    def test_get_team_by_name(self):
        team1 = Team(1, 'team A', 'coach A', 'manager A', 'league A')
        team2 = Team(2, 'team B', 'coach B', 'manager B', 'league B')
        self.service.add_team(team1)
        self.service.add_team(team2)

        self.assertEqual(self.service.get_team_by_name('team A'), team1)
        self.assertEqual(self.service.get_team_by_name('team B'), team2)

    def test_update_team(self):
        team = Team(1, 'team A', 'coach A', 'manager A', 'league A')
        self.service.add_team(team)
        team.name = 'team B'
        self.service.update_team(team)
        self.assertEqual(self.service.get_team(1).name, 'team B')

    def test_delete_team(self):
        team1 = Team(1, 'team A', 'coach A', 'manager A', 'league A')
        team2 = Team(2, 'team B', 'coach B', 'manager B', 'league B')
        team3 = Team(3, 'team C', 'coach C', 'manager C', 'league C')
        self.service.add_team(team1)
        self.service.add_team(team2)
        self.service.add_team(team3)
        self.service.delete_team(1)

        self.assertEqual(len(self.service.list_all_teams()), 2)
        self.assertEqual(self.service.get_team(2), team2)
        self.assertEqual(self.service.get_team(3), team3)

    def test_list_all_teams(self):
        self.service.add_team(Team(1, 'team A', 'coach A', 'manager A', 'league A'))
        self.service.add_team(Team(2, 'team B', 'coach B', 'manager B', 'league B'))
        self.service.add_team(Team(3, 'team C', 'coach C', 'manager C', 'league C'))
        self.assertEqual(len(self.service.list_all_teams()), 3)

    def test_list_all_teams_empty(self):
        self.assertEqual(len(self.service.list_all_teams()), 0)

    def test_list_all_teams_by_league(self):
        self.service.add_team(Team(1, 'team A', 'coach A', 'manager A', 'league A'))
        self.service.add_team(Team(2, 'team B', 'coach B', 'manager B', 'league B'))
        self.service.add_team(Team(3, 'team C', 'coach C', 'manager C', 'league A'))
        self.assertEqual(len(self.service.list_all_teams_by_league('league A')), 2)

    def test_list_all_teams_by_manager(self):
        self.service.add_team(Team(1, 'team A', 'coach A', 'manager A', 'league A'))
        self.service.add_team(Team(2, 'team B', 'coach B', 'manager B', 'league B'))
        self.service.add_team(Team(3, 'team C', 'coach C', 'manager A', 'league C'))
        self.assertEqual(len(self.service.list_all_teams_by_manager('manager A')), 2)

    def test_list_all_teams_by_coach(self):
        self.service.add_team(Team(1, 'team A', 'coach A', 'manager A', 'league A'))
        self.service.add_team(Team(2, 'team B', 'coach B', 'manager B', 'league B'))
        self.service.add_team(Team(3, 'team C', 'coach A', 'manager C', 'league C'))
        self.assertEqual(len(self.service.list_all_teams_by_coach('coach A')), 2)
        