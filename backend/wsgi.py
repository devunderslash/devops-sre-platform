from app import app
import logging
import os

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    port = 5001
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1') # default to localhost - Needs tested
    logger.info(f"Application port used is {port}")
    app.run(host=host, port=port, debug=True)