from entities.player import Player
from repositories.player_repository import PlayerRepository


class PlayerService:
    def __init__(self, repository: PlayerRepository):
        self.repository = repository

    def add_player(self, player: Player) -> None:
        self.repository.add(player)

    def get_player(self, id: int) -> Player:
        return self.repository.get(id)
    
    def get_player_by_name(self, name: str) -> Player:
        return self.repository.get_by_name(name)

    def update_player(self, player: Player) -> None:
        self.repository.update(player)

    def delete_player(self, id: int) -> None:
        self.repository.delete(id)

    def list_all_players(self) -> list[Player]:
        return self.repository.list_all()
    
    def list_all_players_by_year_of_birth(self, year_of_birth: int) -> list[Player]:
        # get player dob and retrieve the year
        return [player for player in self.repository.list_all() if player.dob.year == year_of_birth]
