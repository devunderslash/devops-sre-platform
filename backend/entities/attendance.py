from dataclasses import dataclass, field

@dataclass
class Attendance:
    session_id: int
    player_id: int
    status: str # present, absent, late, etc
    id: int = field(default=None, init=False)  # Optional and auto-generated if not provided
