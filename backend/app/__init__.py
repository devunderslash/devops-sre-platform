import logging

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from config import ConfigFromEnvVars
from app.database import db
from schemas.schemas import player_entity_mapper, team_entity_mapper, session_entity_mapper, attendance_entity_mapper

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] [%(levelname)s] %(message)s',datefmt="%Y-%m-%d %H:%M:%S %z")
logger = logging.getLogger(__name__)


logger.info("Application initialization...")
app = Flask(__name__)

logger.info("Loading configuration...")
app.config.from_object(ConfigFromEnvVars(env_vars=['SECRET_KEY', 'DATABASE_URL', 'SQLALCHEMY_DATABASE_URI', 
                                                   'SQLALCHEMY_TRACK_MODIFICATIONS', ]))


logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")


# Initialize db
db.init_app(app)

# Initialize migration
migrate = Migrate(app, db)

# Map entities to database tables
with app.app_context():
    player_entity_mapper()
    team_entity_mapper()
    session_entity_mapper()
    attendance_entity_mapper()


# Enable CORS
CORS(app)

logger.info("Configuration loaded.")

from routes.base_routes import base_bp
from routes.player_routes import player_bp
from routes.team_routes import team_bp
from routes.session_routes import session_bp
from routes.attendance_routes import attendance_bp

app.register_blueprint(base_bp, url_prefix='/api/v1')
app.register_blueprint(player_bp, url_prefix='/api/v1')
app.register_blueprint(team_bp, url_prefix='/api/v1')
app.register_blueprint(session_bp, url_prefix='/api/v1')
app.register_blueprint(attendance_bp, url_prefix='/api/v1')


# if __name__ == "__main__":
#     app.run(debug=True)