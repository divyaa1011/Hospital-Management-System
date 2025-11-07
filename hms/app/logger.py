"""Basic structured-ish logging (JSON lines friendly)."""

import logging
import json
from .config import Config

class SimpleJsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(base)

def configure_logging():
    level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    handler = logging.FileHandler(Config.LOG_FILE)
    handler.setFormatter(SimpleJsonFormatter())
    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(level)
        root.addHandler(handler)
        root.addHandler(logging.StreamHandler())
    root.info("logging configured", extra={"log_level": Config.LOG_LEVEL})
