from typing import List, Optional

from entities.attendance import Attendance
from repositories.base_repository import Repository


class AttendanceRepository(Repository):
    def __init__(self):
        self.attendances = {}  # In-memory storage for now
        self.next_id = 1

    def get(self, id: int) -> Optional[Attendance]:
        return self.attendances.get(id)

    def add(self, attendance: Attendance) -> None:
        if attendance.id is None:
            attendance.id = self.next_id
            self.next_id += 1
        self.attendances[attendance.id] = attendance

    def update(self, attendance: Attendance) -> None:
        self.attendances[attendance.id] = attendance

    def delete(self, id: int) -> None:
        if id in self.attendances:
            del self.attendances[id]

    def list_all(self) -> List[Attendance]:
        return list(self.attendances.values())