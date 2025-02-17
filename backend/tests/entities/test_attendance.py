from unittest import TestCase

from entities.attendance import Attendance

# @dataclass
# class Attendance:
#     id: int
#     session_id: int
#     player_id: int
#     status: str # present, absent, late, etc

class TestAttendance(TestCase):
    def test_attendance(self):
        attendance = Attendance(session_id=1, player_id=1, status='present')
        self.assertEqual(attendance.session_id, 1)
        self.assertEqual(attendance.player_id, 1)
        self.assertEqual(attendance.status, 'present')
        self.assertEqual(attendance.id, None)
