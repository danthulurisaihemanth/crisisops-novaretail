import logging
from pathlib import Path

def configure_logging() -> logging.Logger:
    logger = logging.getLogger("novaretail")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
    return logger

LOGGER = configure_logging()
