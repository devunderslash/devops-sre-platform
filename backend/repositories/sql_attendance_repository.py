from typing import List, Optional
from entities.attendance import Attendance
from repositories.base_repository import Repository


class SqlAttendanceRepository(Repository):
    def __init__(self, db_session=None):
        self.db_session = db_session

    def get(self, id: int) -> Optional[Attendance]:
        return self.db_session.query(Attendance).filter(Attendance.id == id).first()
    
    def add(self, attendance: Attendance) -> None:
        self.db_session.add(attendance)
        self.db_session.commit()

    def update(self, attendance: Attendance) -> None:
        self.db_session.merge(attendance)
        self.db_session.commit()

    def delete(self, id: int) -> None:
        self.db_session.query(Attendance).filter(Attendance.id == id).delete()
        self.db_session.commit()

    def list_all(self) -> List[Attendance]:
        return self.db_session.query(Attendance).all()
