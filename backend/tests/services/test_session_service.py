from unittest import TestCase
from datetime import datetime

from entities.session import Session
from entities.attendance import Attendance
from repositories.session_repository import SessionRepository
from services.session_service import SessionService


class TestSessionService(TestCase):
    def setUp(self):
        self.service = SessionService(SessionRepository())

    def test_create_session(self):
        self.service.create_session(Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B']))
        self.assertEqual(len(self.service.list_all_sessions()), 1)

    def test_get_session(self):
        session = Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B'])
        self.service.create_session(session)
        self.assertEqual(self.service.get_session(1), session)

    def test_get_session_by_date(self):
        session1 = Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B'])
        session2 = Session(2, datetime(2020, 9, 23, 18, 30, 00), 'location B', 'training', ['team C', 'team D'])
        self.service.create_session(session1)
        self.service.create_session(session2)

        self.assertEqual(self.service.get_session_by_date(datetime(2020, 9, 22, 18, 30, 00)), session1)
        self.assertEqual(self.service.get_session_by_date(datetime(2020, 9, 23, 18, 30, 00)), session2)

    def test_get_session_by_date_not_found(self):
        self.assertIsNone(self.service.get_session_by_date(datetime(2020, 9, 22, 18, 30, 00)))

    def test_update_session(self):
        session = Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B'])
        self.service.create_session(session)
        session.location = 'location B'
        self.service.update_session(session)
        self.assertEqual(self.service.get_session(1).location, 'location B')

    def test_delete_session(self):
        session1 = Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B'])
        session2 = Session(2, datetime(2020, 9, 23, 18, 30, 00), 'location B', 'training', ['team C', 'team D'])
        self.service.create_session(session1)
        self.service.create_session(session2)
        self.service.delete_session(1)

        self.assertEqual(len(self.service.list_all_sessions()), 1)
        self.assertEqual(self.service.get_session(2), session2)

    def test_list_all_sessions(self):
        self.service.create_session(Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B']))
        self.service.create_session(Session(2, datetime(2020, 9, 23, 18, 30, 00), 'location B', 'training', ['team C', 'team D']))
        self.assertEqual(len(self.service.list_all_sessions()), 2)

    def test_list_all_sessions_empty(self):
        self.assertEqual(len(self.service.list_all_sessions()), 0)

    def test_list_all_sessions_by_team(self):
        self.service.create_session(Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B']))
        self.service.create_session(Session(2, datetime(2020, 9, 23, 18, 30, 00), 'location B', 'training', ['team C', 'team D']))
        self.service.create_session(Session(3, datetime(2020, 9, 24, 18, 30, 00), 'location C', 'training', ['team A', 'team D']))
        print(self.service.list_all_sessions())
        print(self.service.list_all_sessions_by_team('team A'))
        self.assertEqual(len(self.service.list_all_sessions_by_team('team A')), 2)
        self.assertEqual(len(self.service.list_all_sessions_by_team('team C')), 1)
        self.assertEqual(len(self.service.list_all_sessions_by_team('team E')), 0)

    def test_add_attendance(self):
        session = Session(1, datetime(2020, 9, 22, 18, 30, 00), 'location A', 'training', ['team A', 'team B'])
        self.service.create_session(session)

        self.service.add_attendance(1, [Attendance(1, 1, 1, 'present'), Attendance(2, 1, 2, 'absent')
                                    , Attendance(3, 1, 3, 'late'), Attendance(4, 1, 4, 'present')])
        self.assertEqual(len(self.service.get_session(1).attendance_records), 4)
