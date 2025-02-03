from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Player:
    id: int
    name: str
    dob: datetime
    joined_group_date: datetime
