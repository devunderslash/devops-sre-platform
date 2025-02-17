# repositories/team_repository.py
from typing import List, Optional
from entities.team import Team
from repositories.base_repository import Repository

class TeamRepository(Repository):
    def __init__(self):
        self.teams = {}  # In-memory storage for now
        self.next_id = 1

    def get(self, id: int) -> Optional[Team]:
        return self.teams.get(id)

    def add(self, team: Team) -> None:
        if team.id is None:
            team.id = self.next_id
            self.next_id += 1
        self.teams[team.id] = team

    def update(self, team: Team) -> None:
        self.teams[team.id] = team

    def delete(self, id: int) -> None:
        if id in self.teams:
            del self.teams[id]

    def list_all(self) -> List[Team]:
        return list(self.teams.values())
    
    # ** Additional methods **
    def get_by_name(self, name: str) -> Optional[Team]:
        for team in self.teams.values():
            if team.name == name:
                return team
        return None
