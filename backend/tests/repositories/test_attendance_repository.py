from unittest import TestCase

from entities.attendance import Attendance
from repositories.attendance_repository import AttendanceRepository


class TestAttendanceRepository(TestCase):
    def setUp(self):
        self.repository = AttendanceRepository()

    def test_add_attendance(self):
        self.repository.add(Attendance(session_id=1, player_id=1, status='present'))
        self.assertEqual(len(self.repository.attendances), 1)

    def test_get_attendance(self):
        attendance = Attendance(session_id=1, player_id=1, status='present')
        self.repository.add(attendance)
        self.assertEqual(self.repository.get(1), attendance)

    def test_update_attendance(self):
        attendance = Attendance(session_id=1, player_id=1, status='present')
        self.repository.add(attendance)
        attendance.status = 'absent'
        self.repository.update(attendance)
        self.assertEqual(self.repository.get(1).status, 'absent')

    def test_delete_attendance(self):
        attendance1 = Attendance(session_id=1, player_id=1, status='present')
        attendance2 = Attendance(session_id=1, player_id=2, status='present')
        attendance3 = Attendance(session_id=2, player_id=1, status='absent')
        self.repository.add(attendance1)
        self.repository.add(attendance2)
        self.repository.add(attendance3)
        self.repository.delete(1)
        print(self.repository.attendances)

        self.assertEqual(len(self.repository.attendances), 2)

    def test_list_all_attendances(self):
        self.repository.add(Attendance(session_id=1, player_id=1, status='present'))
        self.repository.add(Attendance(session_id=2, player_id=2, status='present'))
        self.repository.add(Attendance(session_id=2, player_id=1, status='absent'))
        self.assertEqual(len(self.repository.list_all()), 3)

    
