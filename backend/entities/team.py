from dataclasses import dataclass, field
from typing import List, Optional

from entities.player import Player

@dataclass
class Team:
    name: str
    coach: str
    manager: str
    league: str
    players: Optional[List[Player]] = field(default_factory=list)  # Forward reference
    id: int = field(default=None)  # Optional and auto-generated if not provided