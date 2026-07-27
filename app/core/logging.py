import logging
import sys
from app.core.config import settings

def setup_logging():

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)