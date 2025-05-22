import logging

logger = logging.getLogger("chipchip_logger")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Format
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
console_handler.setFormatter(formatter)

# Add handler if not added already
if not logger.handlers:
    logger.addHandler(console_handler)
