import logging

from config import ConfigFromEnvVars
from flask import Flask
from flask_cors import CORS

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] [%(levelname)s] %(message)s',datefmt="%Y-%m-%d %H:%M:%S %z")

logger = logging.getLogger(__name__)

logger.info("Application initialization...")
app = Flask(__name__)

logger.info("Loading configuration...")

app.config.from_object(ConfigFromEnvVars(env_vars=['SECRET_KEY']))

CORS(app)

logger.info("Configuration loaded.")

from routes.player_routes import player_bp
# from routes.team_routes import team_bp
# from routes.session_routes import session_bp
# from routes.attendance_routes import attendance_bp

app.register_blueprint(player_bp, url_prefix='/api')
# app.register_blueprint(team_bp, url_prefix='/api')
# app.register_blueprint(session_bp, url_prefix='/api')
# app.register_blueprint(attendance_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)