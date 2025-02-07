from dataclasses import dataclass, field

@dataclass
class Attendance:
    id: int = field(init=False)
    session_id: int
    player_id: int
    status: str # present, absent, late, etc
