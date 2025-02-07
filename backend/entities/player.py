from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Player:
    id: int = field(init=False)
    name: str
    dob: datetime
    joined_group_date: datetime
