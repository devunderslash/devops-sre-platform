from dataclasses import dataclass, field
from typing import List

from entities.player import Player

@dataclass
class Team:
    id: int
    name: str
    coach: str
    manager: str
    league: str
    players: List[Player] = field(default_factory=list)  # Forward reference
