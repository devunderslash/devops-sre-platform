from datetime import datetime 
from unittest import TestCase

from entities.session import Session

# @dataclass
# class Session:
#     id: int
#     date: datetime
#     location: str
#     session_type: str # training, match, etc
#     teams: List[str] = field(default_factory=list)  # Team names

class TestSession(TestCase):
    def test_session(self):
        session = Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B'], ['Player 1', 'Player 2'])
        self.assertEqual(session.id, 1)
        self.assertEqual(session.datetime, datetime(2020, 9, 22, 18, 30, 00))
        self.assertEqual(session.location, 'location A')
        self.assertEqual(session.session_type, 'training')
        self.assertEqual(session.teams[0], 'team A')
        self.assertEqual(session.teams[1], 'team B')
        self.assertEqual(session.attendance_records[0], 'Player 1')
