from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from entities.attendance import Attendance

@dataclass
class Player:
    id: int
    name: str
    dob: datetime
    age: int # derived from dob
    joined_group_date: datetime


    def __post_init__(self):
        # Calculate age from dob (example implementation)
        # formayt: dd-mm-yyyy
        dob_date = self.dob
        today = datetime.today()
        self.age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
