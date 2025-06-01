# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
import os
"""
Module de gestion des constantes globales de l'application.
"""

# Variables globales
ENV_TYPE = None
SQLSERVER_CONNECTION_STRING = None
SQLITE_CONNECTION_STRING = None
SFTP_CONFIG = None
OUTPUT_PATHS = None

def load_config():
    """
    Charge les configurations depuis le fichier .env
    et initialise les constantes globales.
    """
    load_dotenv("config.env")
    
    global ENV_TYPE, SQLSERVER_CONNECTION_STRING, SQLITE_CONNECTION_STRING, SFTP_CONFIG, OUTPUT_PATHS
    
    # Type d'environnement
    ENV_TYPE = os.getenv("ENV_TYPE", "development")
    
    # Configuration SQL Server
    SQLSERVER_CONNECTION_STRING = (
        f"DRIVER={os.getenv('SQLSERVER_DRIVER')};"
        f"SERVER={os.getenv('SQLSERVER_HOST')};"
        f"DATABASE={os.getenv('SQLSERVER_DATABASE')};"
        f"UID={os.getenv('SQLSERVER_USER')};"
        f"PWD={os.getenv('SQLSERVER_PASSWORD')}"
    )
    
    # Configuration SQLite
    SQLITE_CONNECTION_STRING = f"sqlite:///{os.getenv('SQLITE_DATABASE')}"
    
    # Configuration SFTP
    SFTP_CONFIG = {
        "host": os.getenv("SFTP_HOST"),
        "port": int(os.getenv("SFTP_PORT", 22)),
        "username": os.getenv("SFTP_USER"),
        "password": os.getenv("SFTP_PASSWORD"),
        "remote_path": os.getenv("SFTP_REMOTE_PATH"),
        "local_path": os.getenv("SFTP_LOCAL_PATH")
    }
    
    # Chemins de sortie
    OUTPUT_PATHS = {
        "csv": os.getenv("CSV_OUTPUT_PATH", "./output/csv"),
        "excel": os.getenv("EXCEL_OUTPUT_PATH", "./output/excel"),
        "pdf": os.getenv("PDF_OUTPUT_PATH", "./output/pdf"),
        "temp": os.getenv("TEMP_PATH", "./temp")
    }
    
    # Création des répertoires s'ils n'existent pas
    for path in OUTPUT_PATHS.values():
        os.makedirs(path, exist_ok=True)

# Constantes de noms de tables
class TableNames:
    """Noms des tables de la base de données."""
    GESTIONNAIRE = "gestionnaire"
    REGION = "region1"
    PAYS = "pays"
    DEVISE = "devise"
    SECTEUR = "secteur"
    SOUS_TYPE_ACTIF = "sous_type_actif1"
    TYPE_ACTIF = "type_actif1"
    SOUS_CLASSIF = "sous_classif1"
    CLASSIF = "classif1"
    TITRE = "titre"
    INDICE = "indice"
    FONDS = "fonds"
    COMPOSITION_FONDS = "composition_fonds_gestionnaire"
    COMPOSITION_PORTEFEUILLE = "composition_portefeuille_gestionnaire"
    COMPOSITION_INDICE = "composition_indice"

# Constantes de colonnes communes
class CommonColumns:
    """Colonnes communes à plusieurs tables."""
    ID = "id"
    CODE = "code"
    NOM = "nom"
    DATE = "date"
    QUANTITE = "quantite"
    PRIX = "prix"
    VALEUR_MARCHANDE = "valeur_marchande"
    ACCRUED = "accrued"
    DIVIDENDE = "dividende"

# Types de fonds
class FundTypes:
    """Types de fonds disponibles."""
    SIMPLE = "simple"
    PORTEFEUILLE = "portefeuille"

# Formats de fichiers supportés
class FileFormats:
    """Formats de fichiers supportés pour l'import/export."""
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"
    ZIP = "zip"
