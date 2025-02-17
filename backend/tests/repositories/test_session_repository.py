from unittest import TestCase
from datetime import datetime

from entities.attendance import Attendance
from entities.session import Session
from repositories.session_repository import SessionRepository


class TestSessionRepository(TestCase):
    def setUp(self):
        self.session_respository = SessionRepository()

    def test_get_session(self):
        session = Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B'])
        self.session_respository.add(session)
        self.assertEqual(self.session_respository.get(1), session)

    def test_get_session_by_date(self):
        session = Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B'])
        self.session_respository.add(session)

    def test_add_session(self):
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B']))
        self.assertEqual(len(self.session_respository.sessions), 1)

    def test_update_session(self):
        session = Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B'])
        self.session_respository.add(session)
        session.location = 'River Pool'
        self.session_respository.update(session)
        self.assertEqual(self.session_respository.get(1).location, 'River Pool')

    def test_delete_session(self):
        session = Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B'])
        self.session_respository.add(session)
        self.session_respository.delete(1)
        self.assertEqual(len(self.session_respository.sessions), 0)

    def test_list_all_sessions(self):
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B']))
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 18, 30), location='River Pool', session_type='training', teams=['team A', 'team B']))
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 19, 30), location='Falls Pool', session_type='training', teams=['team C', 'team B']))
        self.assertEqual(len(self.session_respository.list_all()), 3)

    def test_list_all_sessions_by_team(self):
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B']))
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 18, 30), location='River Pool', session_type='training', teams=['team A', 'team B']))
        self.session_respository.add(Session(datetime=datetime(2024, 4, 22, 19, 30), location='Falls Pool', session_type='training', teams=['team C', 'team B']))
        self.assertEqual(len(self.session_respository.list_all_by_team('team A')), 2)
        self.assertEqual(len(self.session_respository.list_all_by_team('team B')), 3)
        self.assertEqual(len(self.session_respository.list_all_by_team('team C')), 1)

    def test_add_attendance(self):
        session = Session(datetime=datetime(2024, 4, 22, 18, 30), location='Falls Pool', session_type='training', teams=['team A', 'team B'])
        self.session_respository.add(session)

        self.session_respository.add_attendance(1, [Attendance(session_id=1, player_id=1, status='present'), Attendance(session_id=1, player_id=2, status='absent')
                                                    , Attendance(session_id=1, player_id=3, status='late'), Attendance(session_id=1, player_id=4, status='present')])
        self.assertEqual(len(self.session_respository.get(1).attendance_records), 4)
