from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Player:
    name: str
    dob: datetime
    joined_group_date: datetime
    id: int = field(default=None)  # Optional and auto-generated if not provided
