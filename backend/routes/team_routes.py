from flask import Blueprint, request, jsonify
from app import db
from dataclasses import asdict
import logging

from entities.team import Team
from services.team_service import TeamService
from validators.team_validation import TeamValidation
from repositories.sql_team_repository import SqlTeamRepository


logger = logging.getLogger(__name__)

team_bp = Blueprint('team', __name__)

# Initialize repository and service
logger.info("Initializing team repository and service...")
team_repository = SqlTeamRepository(db_session=db.session)
team_service = TeamService(team_repository)


@team_bp.route('/teams', methods=['POST'])
def add_team():
    data = request.json
    errors, validated_data = TeamValidation.validate(data)

    if errors:
        return jsonify(errors), 400

    team = Team(
        name=validated_data['name'],
        league=validated_data['league'],
        manager=validated_data['manager'],
        coach=validated_data['coach'],
        player=validated_data['player']
    )
    logger.info(f"Adding team: {team}")
    team_service.add_team(team)
    return jsonify({"message": "Team added"}), 201

@team_bp.route('/teams', methods=['GET'])
def list_all_teams():
    logger.info("Listing all teams")
    teams = team_service.list_all_teams()
    return jsonify([asdict(team) for team in teams]), 200

@team_bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    logger.info(f"Getting team with id: {id}")
    team = team_service.get_team(id)
    if team:
        return jsonify(asdict(team)), 200
    return jsonify({"error": "Team not found"}), 404

@team_bp.route('/teams/<string:name>', methods=['GET'])
def get_team_by_name(name):
    logger.info(f"Getting team with name: {name}")
    team = team_service.get_team_by_name(name)
    if team:
        return jsonify(asdict(team)), 200
    return jsonify({"error": "Team not found"}), 404

# update
@team_bp.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    data = request.json
    errors, validated_data = TeamValidation.validate(data)

    if errors:
        return jsonify(errors), 400

    team = Team(
        id=id,
        name=validated_data['name'],
        league=validated_data['league'],
        manager=validated_data['manager'],
        coach=validated_data['coach'],
        player=validated_data['player']
    )

    logger.info(f"Updating team with id: {id}")
    team_service.update_team(team)
    return jsonify({"message": "Team updated"}), 200

# delete
@team_bp.route('/teams/<int:id>', methods=['DELETE'])
def delete_team(id):
    logger.info(f"Deleting team with id: {id}")
    team_service.delete_team(id)
    return jsonify({"message": "Team deleted"}), 200
