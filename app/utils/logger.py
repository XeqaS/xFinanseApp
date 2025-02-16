import os
import logging
from logging.handlers import RotatingFileHandler
from config.config import Config

def setup_logger(app):
    if not os.path.exists(Config.LOG_DIR):
        os.mkdir(Config.LOG_DIR)
    
    file_handler = RotatingFileHandler(
        os.path.join(Config.LOG_DIR, Config.LOG_FILE),
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Finance application startup')