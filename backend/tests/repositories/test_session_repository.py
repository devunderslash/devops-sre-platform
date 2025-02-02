from unittest import TestCase
from datetime import datetime

from entities.attendance import Attendance
from entities.session import Session
from repositories.session_repository import SessionRepository


class TestSessionRepository(TestCase):
    def setUp(self):
        self.session_respository = SessionRepository()

    def test_get_session(self):
        session = Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B'])
        self.session_respository.add(session)
        self.assertEqual(self.session_respository.get(1), session)

    def test_get_session_by_date(self):
        session = Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B'])
        self.session_respository.add(session)

    def test_add_session(self):
        self.session_respository.add(Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B']))
        self.assertEqual(len(self.session_respository.sessions), 1)

    def test_update_session(self):
        session = Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B'])
        self.session_respository.add(session)
        session.location = 'River Pool'
        self.session_respository.update(session)
        self.assertEqual(self.session_respository.get(1).location, 'River Pool')

    def test_delete_session(self):
        session = Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B'])
        self.session_respository.add(session)
        self.session_respository.delete(1)
        self.assertEqual(len(self.session_respository.sessions), 0)

    def test_list_all_sessions(self):
        self.session_respository.add(Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B']))
        self.session_respository.add(Session(2, datetime(2024, 4, 22, 18, 30), 'River Pool', 'training', ['team A', 'team B']))
        self.session_respository.add(Session(3, datetime(2024, 4, 22, 19, 30), 'Falls Pool', 'training', ['team C', 'team B']))
        self.assertEqual(len(self.session_respository.list_all()), 3)

    def test_list_all_sessions_by_team(self):
        self.session_respository.add(Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B']))
        self.session_respository.add(Session(2, datetime(2024, 4, 22, 18, 30), 'River Pool', 'training', ['team A', 'team B']))
        self.session_respository.add(Session(3, datetime(2024, 4, 22, 19, 30), 'Falls Pool', 'training', ['team C', 'team B']))
        self.assertEqual(len(self.session_respository.list_all_by_team('team A')), 2)
        self.assertEqual(len(self.session_respository.list_all_by_team('team B')), 3)
        self.assertEqual(len(self.session_respository.list_all_by_team('team C')), 1)

    def test_add_attendance(self):
        session = Session(1, datetime(2024, 4, 22, 18, 30), 'Falls Pool', 'training', ['team A', 'team B'])
        self.session_respository.add(session)

        self.session_respository.add_attendance(1, [Attendance(1, 1, 1, 'present'), Attendance(2, 1, 2, 'absent')
                                                    , Attendance(3, 1, 3, 'late'), Attendance(4, 1, 4, 'present')])
        self.assertEqual(len(self.session_respository.get(1).attendance_records), 4)
