from dataclasses import dataclass, field
from typing import List, Optional

from entities.player import Player

@dataclass
class Team:
    id: int = field(init=False)
    name: str
    coach: str
    manager: str
    league: str
    players: Optional[List[Player]] = field(default_factory=list)  # Forward reference