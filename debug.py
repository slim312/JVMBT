from service import app

# Internal packages:
from logger_init import get_logger
import logging

if __name__ == '__main__':
    logger = get_logger(debug=True, logging_level=logging.DEBUG)
    app.run(debug=True)
    logger.info("Starting server (Debug=True)...")
