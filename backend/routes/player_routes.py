import os
from flask import Blueprint, request, jsonify
from app import db
from dataclasses import asdict
import logging

from entities.player import Player
from services.player_service import PlayerService
from validators.player_validation import PlayerValidation
from services.attendance_service import AttendanceService
from repositories.player_repository import PlayerRepository
from repositories.sql_player_repository import SqlPlayerRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.sql_attendance_repository import SqlAttendanceRepository


logger = logging.getLogger(__name__)

player_bp = Blueprint('player', __name__)

# Initialize repository and service
logger.info("Initializing player repository and service...")
# I want to set up the repositories as the basic repositories for testing purposes, I want a conditional based on the environment
if os.getenv('TESTING') == 'True':
    player_repository = PlayerRepository()
    attendance_repository = AttendanceRepository()
    player_service = PlayerService(player_repository)
    attendance_service = AttendanceService(attendance_repository)
else:
    # to use the SQL repositories
    player_repository = SqlPlayerRepository(db_session=db.session)
    attendance_repository = SqlAttendanceRepository(db_session=db.session)
    player_service = PlayerService(player_repository)
    attendance_service = AttendanceService(attendance_repository)



@player_bp.route('/players', methods=['POST'])
def add_player():
    data = request.json
    errors, validated_data = PlayerValidation.validate(data)

    if errors:
        return jsonify(errors), 400

    player = Player(
        # id needs to be passed as None to be auto-generated    
        name=validated_data['name'],
        dob=validated_data['dob'],
        joined_group_date=validated_data['joined_group_date'],
    )

    player_service.add_player(player)
    return jsonify({"message": "Player added"}), 201


@player_bp.route('/players', methods=['GET'])
def list_all_players():
    players = player_service.list_all_players()
    return jsonify([asdict(player) for player in players]), 200


@player_bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    player = player_service.get_player(id)
    if player:
        return jsonify(asdict(player)), 200
    return jsonify({"error": "Player not found"}), 404

@player_bp.route('/players/<string:name>', methods=['GET'])
def get_player_by_name(name):
    player = player_service.get_player_by_name(name)
    if player:
        return jsonify(asdict(player))
    return jsonify({"error": "Player not found"}), 404


@player_bp.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    data = request.json
    player = Player(
        id=id,
        name=data['name'],
        dob=data['dob'],
        joined_group_date=data['joined_group_date'],
    )
    player_service.update_player(player)
    return jsonify({"message": "Player updated"}), 200


@player_bp.route('/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    player_service.delete_player(id)
    attendance_service.delete_attendance_by_player_id(id)

    return jsonify({"message": "Player deleted"}), 204
