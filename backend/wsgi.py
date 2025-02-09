from app import app
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
        port = 5001
        logger.info(f"Application port used is {port}")
        app.run(host='0.0.0.0', port=port, debug=True)