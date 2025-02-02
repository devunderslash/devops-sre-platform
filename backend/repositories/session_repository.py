from datetime import datetime
from typing import List
from repositories.base_repository import Repository
from entities.session import Session
from entities.attendance import Attendance

class SessionRepository(Repository):
    def __init__(self):
        self.sessions = {}  # In-memory storage for now

    def get(self, id: int) -> Session:
        return self.sessions.get(id)
    
    def get_by_date(self, datetime: datetime) -> Session:
        for session in self.sessions.values():
            if session.datetime == datetime:
                return session
        return None

    def add(self, session: Session) -> None:
        self.sessions[session.id] = session

    def update(self, session: Session) -> None:
        self.sessions[session.id] = session

    def delete(self, id: int) -> None:
        if id in self.sessions:
            del self.sessions[id]

    def list_all(self) -> list[Session]:
        return list(self.sessions.values())
    
    def list_all_by_team(self, team: str) -> list[Session]:
        return [session for session in self.sessions.values() if team in session.teams]
    
    def add_attendance(self, session_id: int, attendance_records: List[Attendance]) -> None:
        session = self.get(session_id)
        if session:
            if not hasattr(session, 'attendance_records'):
                session.attendance_records = []
            session.attendance_records.extend(attendance_records)
