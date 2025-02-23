from flask import Blueprint, request, jsonify
from app import db
from dataclasses import asdict
import logging

from entities.attendance import Attendance
from services.attendance_service import AttendanceService
from repositories.sql_attendance_repository import SqlAttendanceRepository


logger = logging.getLogger(__name__)

attendance_bp = Blueprint('attendance', __name__)

# Initialize repository and service
logger.info("Initializing attendance repository and service...")
attendance_repository = SqlAttendanceRepository(db_session=db.session)
attendance_service = AttendanceService(attendance_repository)


@attendance_bp.route('/attendance', methods=['POST'])
def add_attendance():
    data = request.json
    attendance = Attendance(
        player_id=data['player_id'],
        session_id=data['session_id'],
        status=data['status']
    )
    logger.info(f"Adding attendance: {attendance}")
    attendance_service.add_attendance(attendance)
    return jsonify({"message": "Attendance added"}), 201


@attendance_bp.route('/attendance', methods=['GET'])
def list_all_attendance():
    logger.info("Listing all attendance")
    attendance = attendance_service.list_all_attendance()
    return jsonify([asdict(attendance) for attendance in attendance]), 200


@attendance_bp.route('/attendance/<int:id>', methods=['GET'])
def get_attendance(id):
    logger.info(f"Getting attendance with id: {id}")
    attendance = attendance_service.get_attendance(id)
    if attendance:
        return jsonify(asdict(attendance)), 200
    return jsonify({"error": "Attendance not found"}), 404


@attendance_bp.route('/attendance/<int:player_id>', methods=['GET'])
def get_attendance_by_player(player_id):
    logger.info(f"Getting attendance with player_id: {player_id}")
    attendance = attendance_service.get_attendance_by_player(player_id)
    if attendance:
        return jsonify(asdict(attendance)), 200
    return jsonify({"error": "Attendance not found"}), 404


@attendance_bp.route('/attendance/<int:session_id>', methods=['GET'])
def get_attendance_by_session(session_id):
    logger.info(f"Getting attendance with session_id: {session_id}")
    attendance = attendance_service.get_attendance_by_session(session_id)
    if attendance:
        return jsonify(asdict(attendance)), 200
    return jsonify({"error": "Attendance not found"}), 404


@attendance_bp.route('/attendance/<string:status>', methods=['GET'])
def get_attendance_by_status(status):
    logger.info(f"Getting attendance with status: {status}")
    attendance = attendance_service.get_attendance_by_status(status)
    if attendance:
        return jsonify(asdict(attendance)), 200
    return jsonify({"error": "Attendance not found"}), 404


@attendance_bp.route('/attendance/<int:id>', methods=['PUT'])
def update_attendance(id):
    data = request.json
    attendance = Attendance(
        id=id,
        player_id=data['player_id'],
        session_id=data['session_id'],
        status=data['status']
    )
    logger.info(f"Updating attendance: {attendance}")
    attendance_service.update_attendance(attendance)
    return jsonify({"message": "Attendance updated"}), 200

# delete
@attendance_bp.route('/attendance/<int:id>', methods=['DELETE'])
def delete_attendance(id):
    logger.info(f"Deleting attendance with id: {id}")
    attendance_service.delete_attendance(id)
    return jsonify({"message": "Attendance deleted"}), 200

@attendance_bp.route('/attendance/<int:session_id>', methods=['DELETE'])
def delete_attendance_by_session(session_id):
    logger.info(f"Deleting attendance with session_id: {session_id}")
    attendance_service.delete_attendance_by_session(session_id)
    return jsonify({"message": "Attendance deleted"}), 200
