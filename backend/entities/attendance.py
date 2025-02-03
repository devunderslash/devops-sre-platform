from dataclasses import dataclass

@dataclass
class Attendance:
    id: int
    session_id: int
    player_id: int
    status: str # present, absent, late, etc
