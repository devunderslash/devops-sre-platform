from flask import Blueprint, request, jsonify
from app import db
from dataclasses import asdict
import logging

from entities.session import Session
from services.session_service import SessionService
from validators.session_validation import SessionValidation
from repositories.sql_session_repository import SqlSessionRepository


logger = logging.getLogger(__name__)

session_bp = Blueprint('session', __name__)

# Initialize repository and service
logger.info("Initializing session repository and service...")
session_repository = SqlSessionRepository(db_session=db.session)
session_service = SessionService(session_repository)


@session_bp.route('/sessions', methods=['POST'])
def add_session():
    data = request.json
    errors, validated_data = SessionValidation.validate(data)

    if errors:
        return jsonify(errors), 400

    session = Session(
        datetime=validated_data['datetime'],
        location=validated_data['location'],
        teams=validated_data['teams'],
        attendance_records=validated_data['attendance_records']
    )
    logger.info(f"Adding session: {session}")
    session_service.add_session(session)
    return jsonify({"message": "Session added"}), 201


@session_bp.route('/sessions', methods=['GET'])
def list_all_sessions():
    logger.info("Listing all sessions")
    sessions = session_service.list_all_sessions()
    return jsonify([asdict(session) for session in sessions]), 200


@session_bp.route('/sessions/<int:id>', methods=['GET'])
def get_session(id):
    logger.info(f"Getting session with id: {id}")
    session = session_service.get_session(id)
    if session:
        return jsonify(asdict(session)), 200
    return jsonify({"error": "Session not found"}), 404

@session_bp.route('/sessions/<string:datetime>', methods=['GET'])
def get_session_by_date(datetime):
    logger.info(f"Getting session with date: {datetime}")
    session = session_service.get_session_by_date(datetime)
    if session:
        return jsonify(asdict(session)), 200
    return jsonify({"error": "Session not found"}), 404

# update
@session_bp.route('/sessions/<int:id>', methods=['PUT'])
def update_session(id):
    data = request.json
    errors, validated_data = SessionValidation.validate(data)

    if errors:
        return jsonify(errors), 400

    session = Session(
        id=id,
        datetime=validated_data['datetime'],
        location=validated_data['location'],
        teams=validated_data['teams'],
        attendance_records=validated_data['attendance_records']
    )
    logger.info(f"Updating session: {session}")
    session_service.update_session(session)
    return jsonify({"message": "Session updated"}), 200

# delete
@session_bp.route('/sessions/<int:id>', methods=['DELETE'])
def delete_session(id):
    logger.info(f"Deleting session with id: {id}")
    session_service.delete_session(id)
    return jsonify({"message": "Session deleted"}), 200
