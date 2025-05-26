# logic/data_import_logic.py

import os
import pandas as pd
from STFP.sftp import SFTPClient
import logging
from utils import csv, excel # Assuming these modules exist with required functions
from utils import data
from database.connexionsqlServer import SQLServerConnection
from database.connexionsqlLiter import SQLiteConnection
from constantes import const1
import logging
# Configuration du logger
logger = logging.getLogger(__name__)

# Configuration du logger
async def import_data_from_sftp(remote_filepath: str, local_filepath: str, target_table_name: str):
    """
    Importe un fichier depuis un serveur SFTP vers un chemin local.

    Args:
        remote_filepath (str): Le chemin du fichier sur le serveur SFTP.
        local_filepath (str): Le chemin local où enregistrer le fichier.
 target_table_name (str): Le nom de la table cible dans la base de données.
    """
    sftp_client = None
    try:
        # 1. Se connecter au SFTP
        logger.info(f"Attempting to connect to SFTP server...")
        sftp_client = SFTPClient()
        await sftp_client.connect()
        logger.info(f"Successfully connected to SFTP server.")

        # 2. Télécharger le fichier spécifié
        logger.info(f"Attempting to download file from {remote_filepath} to {local_filepath}...")
        await sftp_client.download_file(remote_filepath, local_filepath)
        logger.info(f"File downloaded successfully from {remote_filepath} to {local_filepath}.")

        # Déterminer l'extension du fichier et le lire
        file_extension = os.path.splitext(local_filepath)[1].lower()

        dataframe = None
        if file_extension == '.csv':
            logger.info(f"Reading CSV file: {local_filepath}")
            dataframe = csv.load_csv_to_dataframe(local_filepath)
            logger.info(f"CSV file read successfully. DataFrame shape: {dataframe.shape}")
        elif file_extension in ['.xlsx', '.xls']:
            logger.info(f"Reading Excel file: {local_filepath}")
            dataframe = excel.load_excel_to_dataframe(local_filepath)
            logger.info(f"Excel file read successfully. DataFrame shape: {dataframe.shape}")
        else:
            logger.error(f"Unsupported file extension: {file_extension}")
            # Optionally, raise an exception or return an error indicator
            raise ValueError(f"Unsupported file type for import: {file_extension}")

        # 1. Obtenir la connexion à la base de données appropriée
        db_connection = None
        try:
            if const1.ENV_TYPE == "prod": # Assuming "dev" or any other value means SQLite
 logger.info("Using SQL Server connection for database operations.")
 db_connection = SQLServerConnection()
 else:
 logger.info("Using SQLite connection for database operations.")
 db_connection = SQLiteConnection()

            # Ouvre la connexion à la base de données
            await db_connection.open_connection()
            logger.info("Database connection opened.")


 # 3. Charger les données dans la base de données
 logger.info(f"Attempting to load data into table: {target_table_name}")
 data.load_dataframe_to_sql(dataframe, target_table_name, db_connection.engine)

    except Exception as e:
        logger.error(f"An error occurred during SFTP import: {e}", exc_info=True)
        raise  # Relaisser l'exception pour qu'elle soit gérée par l'appelant
    finally:
        # 4. Se déconnecter du SFTP
        if sftp_client:
            await sftp_client.disconnect()
            logger.info("SFTP connection closed.")
        if db_connection:
            await db_connection.close_connection()
            logger.info("Database connection closed.")
