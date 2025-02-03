from unittest import TestCase

from entities.attendance import Attendance
from services.attendance_service import AttendanceService


class TestAttendanceService(TestCase):
    def setUp(self):
        self.service = AttendanceService()

    def test_add_attendance(self):
        self.service.add_attendance(Attendance(1, 1, 1, 'present'))
        self.service.add_attendance(Attendance(2, 1, 2, 'absent'))
        self.assertEqual(len(self.service.list_all_attendances()), 2)

    def test_get_attendance(self):
        attendance = Attendance(1, 1, 1, 'present')
        self.service.add_attendance(attendance)
        self.assertEqual(self.service.get_attendance(1), attendance)

    def test_get_attendance_by_session(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 2, 1, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.assertEqual(self.service.get_attendance_by_session(1), [attendance1, attendance2])
        self.assertEqual(self.service.get_attendance_by_session(2), [attendance3])

    def test_get_attendance_by_player(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 2, 1, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.assertEqual(self.service.get_attendance_by_player(1), [attendance1, attendance3])
        self.assertEqual(self.service.get_attendance_by_player(2), [attendance2])

    def test_get_attendance_by_status(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 2, 1, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.assertEqual(self.service.get_attendance_by_status('present'), [attendance1])
        self.assertEqual(self.service.get_attendance_by_status('absent'), [attendance2])
        self.assertEqual(self.service.get_attendance_by_status('late'), [attendance3])

    def test_update_attendance(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        attendance1.status = 'late'
        attendance2.status = 'present'
        self.service.update_attendance(attendance1)
        self.service.update_attendance(attendance2)

        self.assertEqual(self.service.get_attendance(1).status, 'late')
        self.assertEqual(self.service.get_attendance(2).status, 'present')

    def test_update_attendance_by_session_id(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 2, 1, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.service.update_attendance_by_session_id(1, 'late')

        self.assertEqual(self.service.get_attendance(1).status, 'late')
        self.assertEqual(self.service.get_attendance(2).status, 'late')


    def test_delete_attendance(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 1, 3, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.service.delete_attendance(1)

        self.assertEqual(len(self.service.list_all_attendances()), 2)
        self.assertEqual(self.service.get_attendance(2), attendance2)
        self.assertEqual(self.service.get_attendance(3), attendance3)

    def test_delete_attendance_by_player_id(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 1, 3, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.service.delete_attendance_by_player_id(1)

        self.assertEqual(len(self.service.list_all_attendances()), 2)
        self.assertEqual(self.service.get_attendance(2), attendance2)

    def test_delete_attendance_by_session(self):
        attendance1 = Attendance(1, 1, 1, 'present')
        attendance2 = Attendance(2, 1, 2, 'absent')
        attendance3 = Attendance(3, 2, 1, 'late')
        self.service.add_attendance(attendance1)
        self.service.add_attendance(attendance2)
        self.service.add_attendance(attendance3)
        self.service.delete_attendance_by_session(1)

        self.assertEqual(len(self.service.list_all_attendances()), 1)
        self.assertEqual(self.service.get_attendance(3), attendance3)

    def test_list_all_attendances(self):
        self.service.add_attendance(Attendance(1, 1, 1, 'present'))
        self.service.add_attendance(Attendance(2, 1, 2, 'absent'))
        self.assertEqual(len(self.service.list_all_attendances()), 2)

    def test_list_all_attendances_empty(self):
        self.assertEqual(len(self.service.list_all_attendances()), 0)