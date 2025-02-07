from typing import List, Optional
from entities.player import Player
from repositories.base_repository import Repository


class SqlPlayerRepository(Repository):
    def __init__(self, db_session=None):
        self.db_session = db_session

    def get(self, id: int) -> Optional[Player]:
        return self.db_session.query(Player).filter(Player.id == id).first()
    
    def add(self, player: Player) -> None:
        self.db_session.add(player)
        self.db_session.commit()

    def update(self, player: Player) -> None:
        self.db_session.merge(player)
        self.db_session.commit()

    def delete(self, id: int) -> None:
        self.db_session.query(Player).filter(Player.id == id).delete()
        self.db_session.commit()

    def list_all(self) -> List[Player]:
        return self.db_session.query(Player).all()
    
    def get_by_name(self, name: str) -> Optional[Player]:
        return self.db_session.query(Player).filter(Player.name == name).first()
    