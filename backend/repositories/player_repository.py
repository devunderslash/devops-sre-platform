from typing import List, Optional
from entities.player import Player
from repositories.base_repository import Repository

class PlayerRepository(Repository):
    def __init__(self):
        self.players = {}
        self.next_id = 1

    def get(self, id: int) -> Optional[Player]:
        return self.players.get(id)

    def add(self, player: Player) -> None:
        if player.id is None:
            player.id = self.next_id
            self.next_id += 1
        self.players[player.id] = player

    def update(self, player: Player) -> None:
        self.players[player.id] = player

    def delete(self, id: int) -> None:
        if id in self.players:
            del self.players[id]

    def list_all(self) -> List[Player]:
        return list(self.players.values())
    
    # ** Additional methods **
    
    def get_by_name(self, name: str) -> Optional[Player]:
        for player in self.players.values():
            if player.name == name:
                return player
        return None
