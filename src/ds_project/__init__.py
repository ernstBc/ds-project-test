import os
import sys
import logging

logging_format = "%(asctime)s - %(levelname)s: %(module)s - %(message)s"
log_dir = 'logs'
log_path = os.path.join(log_dir, 'app.log')

os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format=logging_format,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('project_logger')
logger.info("Logging setup complete.")