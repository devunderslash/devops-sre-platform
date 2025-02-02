from datetime import datetime
from typing import List
from entities.attendance import Attendance
from entities.session import Session
from repositories.session_repository import SessionRepository


class SessionService:
    def __init__(self):
        self.repository = SessionRepository()

    def create_session(self, session: Session) -> None:
        self.repository.add(session)

    def get_session(self, id: int) -> Session:
        return self.repository.get(id)
    
    def get_session_by_date(self, datetime: datetime) -> Session:
        return self.repository.get_by_date(datetime)
    
    def update_session(self, session: Session) -> None:
        self.repository.update(session)

    def delete_session(self, id: int) -> None:
        self.repository.delete(id)

    def list_all_sessions(self) -> list[Session]:
        return self.repository.list_all()
    
    def list_all_sessions_by_team(self, team: str) -> list[Session]:
        return [session for session in self.repository.list_all() if team in session.teams]
    
    # def list_all_sessions_by_location(self, location: str) -> list[Session]:
    #     return [session for session in self.repository.list_all() if session.location == location]
    
    # def list_all_sessions_by_type(self, session_type: str) -> list[Session]:
    #     return [session for session in self.repository.list_all() if session.session_type == session_type]
    
    def add_attendance(self, session_id: int, attendance: List[Attendance]) -> None:
        self.repository.add_attendance(session_id, attendance)