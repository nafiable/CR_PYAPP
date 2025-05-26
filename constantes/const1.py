# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
import os
"""
Module pour stocker les constantes de l'application.
"""

# Constantes de configuration (placeholders qui seront chargés depuis config.env)
BD_SERVER = ""
BD_NAME = ""
BD_USER = ""
BD_PASSWORD = ""
SQLITE_DB_PATH = ""
ENV_TYPE = "" # 'dev' ou 'prod'
LOG_PATH = ""

# Exemples de constantes hardcodées
SFTP_HOSTNAME = ""
SFTP_PORT = ""
SFTP_USERNAME = ""
SFTP_PASSWORD = ""

DEFAULT_BUFFER_SIZE = 4096
API_VERSION = "1.0"

def load_config():
    """
    Charge les variables de configuration depuis le fichier config.env
    Ajoute des logs pour indiquer le chargement et les valeurs (en mode debug).
    """
    load_dotenv(dotenv_path='config.env')

    global BD_SERVER, BD_NAME, BD_USER, BD_PASSWORD, SQLITE_DB_PATH, ENV_TYPE, LOG_PATH, \
        SFTP_HOSTNAME, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD

    BD_SERVER = os.getenv("BD_SERVER")
    BD_NAME = os.getenv("BD_NAME")
    BD_USER = os.getenv("BD_USER")
    BD_PASSWORD = os.getenv("BD_PASSWORD")
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")
    ENV_TYPE = os.getenv("ENV_TYPE")
    LOG_PATH = os.getenv("LOG_PATH")
    SFTP_HOSTNAME = os.getenv("SFTP_HOSTNAME")
    SFTP_PORT = os.getenv("SFTP_PORT")
    SFTP_USERNAME = os.getenv("SFTP_USERNAME")
    SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")

    logger.info("Configuration loaded from config.env")
    logger.debug(f"BD_SERVER: {BD_SERVER}")
    logger.debug(f"BD_NAME: {BD_NAME}")
    logger.debug(f"BD_USER: {BD_USER}")
    # Avoid logging sensitive info like passwords at higher levels
    logger.debug("BD_PASSWORD: [REDACTED]")
    logger.debug(f"SQLITE_DB_PATH: {SQLITE_DB_PATH}")
    logger.debug(f"ENV_TYPE: {ENV_TYPE}")
    logger.debug(f"LOG_PATH: {LOG_PATH}")
    logger.debug("SFTP_ credentials loaded (details not logged)")
