from flask import Blueprint, jsonify
import logging


logger = logging.getLogger(__name__)

base_bp = Blueprint('base', __name__)

# Checking health of the application
@base_bp.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check")
    return jsonify({"message": "Healthy"}), 200
