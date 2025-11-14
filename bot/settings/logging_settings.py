import logging
from logging.handlers import RotatingFileHandler
import os

from bot.settings.paths import LOGS_DIR

os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "tuition.log")

LOG_FORMAT = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger("tuition")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1_000_000,  
    backupCount=10,       
    encoding="utf-8",
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)