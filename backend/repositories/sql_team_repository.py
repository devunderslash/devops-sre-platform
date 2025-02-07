from typing import List, Optional
from entities.team import Team
from repositories.base_repository import Repository

class SqlTeamRepository(Repository):
    def __init__(self, db_session=None):
        self.db_session = db_session

    def get(self, id: int) -> Optional[Team]:
        return self.db_session.query(Team).filter(Team.id == id).first()
    
    def add(self, team: Team) -> None:
        self.db_session.add(team)
        self.db_session.commit()

    def update(self, team: Team) -> None:
        self.db_session.merge(team)
        self.db_session.commit()

    def delete(self, id: int) -> None:
        self.db_session.query(Team).filter(Team.id == id).delete()
        self.db_session.commit()

    def list_all(self) -> List[Team]:
        return self.db_session.query(Team).all()
    
    def get_by_name(self, name: str) -> Optional[Team]:
        return self.db_session.query(Team).filter(Team.name == name).first()
    
    def get_by_coach(self, coach: str) -> Optional[Team]:
        return self.db_session.query(Team).filter(Team.coach == coach).first()
    
    def get_by_player(self, player: str) -> Optional[Team]:
        return self.db_session.query(Team).filter(Team.player == player).first()
