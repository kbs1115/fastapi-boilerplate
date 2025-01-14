# app/core/logging_conf.py
import logging
import logging.config
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE),
            "formatter": "standard",
            "level": "INFO",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING)
