from unittest import TestCase

from entities.attendance import Attendance
from repositories.attendance_repository import AttendanceRepository


class TestAttendanceRepository(TestCase):
    def setUp(self):
        self.repository = AttendanceRepository()

    def test_add_attendance(self):
        self.repository.add(Attendance(1, 1, 1, 'present'))
        self.assertEqual(len(self.repository.attendances), 1)

    def test_get_attendance(self):
        attendance = Attendance(1, 1, 1, 'present')
        self.repository.add(attendance)
        self.assertEqual(self.repository.get(1), attendance)

    def test_update_attendance(self):
        attendance = Attendance(1, 1, 1, 'present')
        self.repository.add(attendance)
        attendance.status = 'absent'
        self.repository.update(attendance)
        self.assertEqual(self.repository.get(1).status, 'absent')

    def test_delete_attendance(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'present')
        attendance3 = Attendance(3, 2, 1, 'absent')
        self.repository.add(attendance1)
        self.repository.add(attendance2)
        self.repository.add(attendance3)
        self.repository.delete(1)

        self.assertEqual(len(self.repository.attendances), 2)
        self.assertEqual(self.repository.get(2), attendance2)
        self.assertEqual(self.repository.get(3), attendance3)

    def test_list_all_attendances(self):
        self.repository.add(Attendance(1, 1, 1, 'present'))
        self.repository.add(Attendance(2, 1, 2, 'present'))
        self.repository.add(Attendance(3, 2, 1, 'absent'))
        self.assertEqual(len(self.repository.list_all()), 3)

    
