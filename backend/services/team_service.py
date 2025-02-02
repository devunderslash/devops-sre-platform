from entities.team import Team
from repositories.team_repository import TeamRepository


class TeamService:
    def __init__(self):
        self.repository = TeamRepository()

    def add_team(self, team: Team) -> None:
        self.repository.add(team)

    def get_team(self, id: int) -> Team:
        return self.repository.get(id)
    
    def get_team_by_name(self, name: str) -> Team:
        return self.repository.get_by_name(name)

    def update_team(self, team: Team) -> None:
        self.repository.update(team)

    def delete_team(self, id: int) -> None:
        self.repository.delete(id)

    def list_all_teams(self) -> list[Team]:
        return self.repository.list_all()
    
    def list_all_teams_by_league(self, league: str) -> list[Team]:
        return [team for team in self.repository.list_all() if team.league == league]
    
    def list_all_teams_by_manager(self, manager: str) -> list[Team]:
        return [team for team in self.repository.list_all() if team.manager == manager]
    
    def list_all_teams_by_coach(self, coach: str) -> list[Team]:
        return [team for team in self.repository.list_all() if team.coach == coach]
