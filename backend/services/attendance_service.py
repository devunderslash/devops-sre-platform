from entities.attendance import Attendance
from repositories.attendance_repository import AttendanceRepository

class AttendanceService:
    def __init__(self):
        self.repository = AttendanceRepository()

    def add_attendance(self, attendance: Attendance) -> None:
        self.repository.add(attendance)

    def get_attendance(self, id: int) -> Attendance:
        return self.repository.get(id)
    
    def get_attendance_by_session(self, session_id: int) -> list[Attendance]:
        return [attendance for attendance in self.repository.list_all() if attendance.session_id == session_id]
    
    def get_attendance_by_player(self, player_id: int) -> list[Attendance]:
        return [attendance for attendance in self.repository.list_all() if attendance.player_id == player_id]
    
    def get_attendance_by_status(self, status: str) -> list[Attendance]:
        return [attendance for attendance in self.repository.list_all() if attendance.status == status]
    
    def update_attendance(self, attendance: Attendance) -> None:
        self.repository.update(attendance)

    def update_attendance_by_session_id(self, session_id: int, status: str) -> None:
        for attendance in self.repository.list_all():
            if attendance.session_id == session_id:
                attendance.status = status
                self.repository.update(attendance)

    def delete_attendance(self, id: int) -> None:
        self.repository.delete(id)

    def delete_attendance_by_session(self, session_id: int) -> None:
        for attendance in self.repository.list_all():
            if attendance.session_id == session_id:
                self.repository.delete(attendance.id)

    def delete_attendance_by_player_id(self, player_id: int) -> None:
        for attendance in self.repository.list_all():
            if attendance.player_id == player_id:
                self.repository.delete(attendance.id)

    def list_all_attendances(self) -> list[Attendance]:
        return self.repository.list_all()
    