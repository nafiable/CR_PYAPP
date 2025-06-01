"""
Configuration du système de logging de l'application.
"""

import os
import logging.config
from pathlib import Path

def setup_logging():
    """Configure le système de logging."""
    
    # Création du répertoire des logs s'il n'existe pas
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configuration du logging
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "./logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": "./logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file", "error_file"],
                "level": os.getenv("LOG_LEVEL", "INFO"),
                "propagate": True
            },
            "sqlalchemy.engine": {
                "handlers": ["file"],
                "level": "WARNING",
                "propagate": False
            },
            "fastapi": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": False
            }
        }
    }
    
    # Application de la configuration
    logging.config.dictConfig(config)
    
    # Logger pour ce module
    logger = logging.getLogger(__name__)
    logger.info("Configuration du logging terminée") 