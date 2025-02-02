from flask import Blueprint, request, jsonify

from entities.player import Player
from services.player_service import PlayerService
from validators.player_validation import PlayerValidation
from services.attendance_service import AttendanceService
from repositories.player_repository import PlayerRepository
from repositories.attendance_repository import AttendanceRepository

player_bp = Blueprint('player', __name__)

# Initialize repository and service
player_repository = PlayerRepository()
attendance_repository = AttendanceRepository()
player_service = PlayerService(player_repository)
attendance_service = AttendanceService()


@player_bp.route('/players', methods=['POST'])
def add_player():
    data = request.json
    errors, validated_data = PlayerValidation.validate(data)

    if errors:
        return jsonify(errors), 400

    player = Player(
        id=validated_data['id'],
        name=validated_data['name'],
        dob=validated_data['dob'],
        age=validated_data['age'],
        joined_group_date=validated_data['joined_group_date'],

    )
    player_service.add_player(player)
    return jsonify({"message": "Player added"}), 201


@player_bp.route('/players', methods=['GET'])
def list_all_players():
    players = player_service.list_all_players()
    return jsonify([player.__dict__ for player in players]), 200


@player_bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    player = player_service.get_player(id)
    if player:
        return jsonify(player.__dict__)
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

    return jsonify({"message": "Player deleted"}), 200


@player_bp.route('/players/<string:name>', methods=['GET'])
def get_player_by_name(name):
    player = player_service.get_player_by_name(name)
    if player:
        return jsonify(player.__dict__)
    return jsonify({"error": "Player not found"}), 404