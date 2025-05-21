import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Create logger
logger = logging.getLogger("chipchip_logger")
logger.setLevel(logging.INFO)

# Set daily rotating handler (rotates at midnight)
handler = TimedRotatingFileHandler(
    "logs/app.log", when="midnight", interval=1, backupCount=7
)
handler.suffix = "%Y-%m-%d"  # file name format: app.log.2025-05-21
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
