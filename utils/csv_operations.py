"""
Module de gestion des opérations sur les fichiers CSV.
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
from sqlalchemy.engine import Engine
from database.connexionsqlServer import SQLServerConnection
from database.connexionsqlLiter import SQLiteConnection

logger = logging.getLogger(__name__)

class CSVOperations:
    """Classe pour gérer les opérations sur les fichiers CSV."""
    
    def __init__(self):
        """Initialisation des connexions aux bases de données."""
        self.sql_server = SQLServerConnection()
        self.sqlite = SQLiteConnection()
    
    def read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Lit un fichier CSV et retourne un DataFrame.
        
        Args:
            file_path (str): Chemin du fichier CSV
            **kwargs: Arguments supplémentaires pour pd.read_csv
            
        Returns:
            pd.DataFrame: DataFrame contenant les données
        """
        try:
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Fichier CSV lu avec succès : {file_path}")
            return df
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du CSV {file_path}: {str(e)}")
            raise
    
    def write_csv(self, df: pd.DataFrame, file_path: str, **kwargs) -> None:
        """
        Écrit un DataFrame dans un fichier CSV.
        
        Args:
            df (pd.DataFrame): DataFrame à sauvegarder
            file_path (str): Chemin du fichier CSV
            **kwargs: Arguments supplémentaires pour df.to_csv
        """
        try:
            # Créer le répertoire si nécessaire
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(file_path, **kwargs)
            logger.info(f"DataFrame sauvegardé en CSV : {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du CSV {file_path}: {str(e)}")
            raise
    
    def csv_to_excel(self, csv_path: str, excel_path: str, **kwargs) -> None:
        """
        Convertit un fichier CSV en fichier Excel.
        
        Args:
            csv_path (str): Chemin du fichier CSV source
            excel_path (str): Chemin du fichier Excel destination
            **kwargs: Arguments supplémentaires pour pd.read_csv
        """
        try:
            df = self.read_csv(csv_path, **kwargs)
            df.to_excel(excel_path, index=False)
            logger.info(f"CSV converti en Excel : {excel_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la conversion CSV->Excel: {str(e)}")
            raise
    
    def csv_to_sql_server(self, csv_path: str, table_name: str, if_exists: str = 'fail', **kwargs) -> None:
        """
        Importe un fichier CSV dans SQL Server.
        
        Args:
            csv_path (str): Chemin du fichier CSV
            table_name (str): Nom de la table
            if_exists (str): Comportement si la table existe ('fail', 'replace', 'append')
            **kwargs: Arguments supplémentaires pour pd.read_csv
        """
        try:
            df = self.read_csv(csv_path, **kwargs)
            with self.sql_server.get_connection() as conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            logger.info(f"CSV importé dans SQL Server : {table_name}")
        except Exception as e:
            logger.error(f"Erreur lors de l'import CSV->SQL Server: {str(e)}")
            raise
    
    def csv_to_sqlite(self, csv_path: str, table_name: str, if_exists: str = 'fail', **kwargs) -> None:
        """
        Importe un fichier CSV dans SQLite.
        
        Args:
            csv_path (str): Chemin du fichier CSV
            table_name (str): Nom de la table
            if_exists (str): Comportement si la table existe ('fail', 'replace', 'append')
            **kwargs: Arguments supplémentaires pour pd.read_csv
        """
        try:
            df = self.read_csv(csv_path, **kwargs)
            with self.sqlite.get_connection() as conn:
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            logger.info(f"CSV importé dans SQLite : {table_name}")
        except Exception as e:
            logger.error(f"Erreur lors de l'import CSV->SQLite: {str(e)}")
            raise
    
    def sql_to_csv(self, query: str, csv_path: str, is_sqlite: bool = False, **kwargs) -> None:
        """
        Exporte le résultat d'une requête SQL vers un fichier CSV.
        
        Args:
            query (str): Requête SQL
            csv_path (str): Chemin du fichier CSV
            is_sqlite (bool): True pour SQLite, False pour SQL Server
            **kwargs: Arguments supplémentaires pour df.to_csv
        """
        try:
            conn = self.sqlite if is_sqlite else self.sql_server
            with conn.get_connection() as connection:
                df = pd.read_sql_query(query, connection)
                self.write_csv(df, csv_path, **kwargs)
            logger.info(f"Données SQL exportées en CSV : {csv_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'export SQL->CSV: {str(e)}")
            raise
    
    @staticmethod
    def df_to_csv(df: pd.DataFrame, csv_path: str, **kwargs) -> None:
        """
        Convertit un DataFrame en fichier CSV.
        
        Args:
            df (pd.DataFrame): DataFrame à convertir
            csv_path (str): Chemin du fichier CSV
            **kwargs: Arguments supplémentaires pour df.to_csv
        """
        try:
            Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(csv_path, **kwargs)
            logger.info(f"DataFrame converti en CSV : {csv_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la conversion DataFrame->CSV: {str(e)}")
            raise 