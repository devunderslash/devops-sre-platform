from datetime import datetime
from typing import List, Optional
from entities.session import Session
from entities.attendance import Attendance
from repositories.base_repository import Repository

class SqlSessionRepository(Repository):
    def __init__(self, db_session=None):
        self.db_session = db_session

    def get(self, id: int) -> Optional[Session]:
        return self.db_session.query(Session).filter(Session.id == id).first()
    
    def add(self, session: Session) -> None:
        self.db_session.add(session)
        self.db_session.commit()

    def update(self, session: Session) -> None:
        self.db_session.merge(session)
        self.db_session.commit()

    def delete(self, id: int) -> None:
        self.db_session.query(Session).filter(Session.id == id).delete()
        self.db_session.commit()

    def list_all(self) -> List[Session]:
        return self.db_session.query(Session).all()
    
    def get_by_date(self, datetime: datetime) -> Optional[Session]:
        return self.db_session.query(Session).filter(Session.datetime == datetime).first()
    
    def list_all_by_team(self, team: str) -> List[Session]:
        return self.db_session.query(Session).filter(Session.teams.contains(team)).all()
    
    def add_attendance(self, session_id: int, attendance_records: List[Attendance]) -> None:
        session = self.get(session_id)
        if session:
            session.attendance_records.extend(attendance_records)
