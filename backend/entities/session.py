from dataclasses import dataclass, field
from typing import List
from datetime import datetime

from entities.attendance import Attendance


@dataclass
class Session:
    datetime: datetime
    location: str
    session_type: str # training, match, etc
    teams: List[str] = field(default_factory=list)  # Team names
    attendance_records: List[Attendance] = field(default_factory=list)  # Attendance records
    id: int = field(default=None)  # Optional and auto-generated if not provided

