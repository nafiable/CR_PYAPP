"""
Module de gestion des fichiers CSV.
"""

import logging
import pandas as pd
from typing import Dict, List, Union, Optional
from pathlib import Path
import sqlite3
import pyodbc
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

class CSVManager:
    """Gestionnaire de fichiers CSV."""
    
    def __init__(self, encoding: str = 'utf-8', separator: str = ';'):
        """
        Initialise le gestionnaire CSV.
        
        Args:
            encoding (str): Encodage des fichiers
            separator (str): Séparateur CSV
        """
        self.encoding = encoding
        self.separator = separator
    
    def read_csv(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Lit un fichier CSV.
        
        Args:
            file_path: Chemin du fichier
            **kwargs: Arguments additionnels pour pd.read_csv
            
        Returns:
            DataFrame: Données du CSV
        """
        try:
            df = pd.read_csv(
                file_path,
                encoding=self.encoding,
                sep=self.separator,
                **kwargs
            )
            logger.info(f"Fichier CSV lu avec succès: {file_path}")
            return df
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du CSV {file_path}: {str(e)}")
            raise
    
    def write_csv(self, df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
        """
        Écrit un DataFrame dans un fichier CSV.
        
        Args:
            df: DataFrame à sauvegarder
            file_path: Chemin du fichier
            **kwargs: Arguments additionnels pour df.to_csv
        """
        try:
            df.to_csv(
                file_path,
                encoding=self.encoding,
                sep=self.separator,
                index=False,
                **kwargs
            )
            logger.info(f"DataFrame sauvegardé en CSV: {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du CSV {file_path}: {str(e)}")
            raise
    
    def to_excel(self, df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
        """
        Convertit un DataFrame en fichier Excel.
        
        Args:
            df: DataFrame à convertir
            file_path: Chemin du fichier Excel
            **kwargs: Arguments additionnels pour df.to_excel
        """
        try:
            df.to_excel(file_path, index=False, **kwargs)
            logger.info(f"DataFrame converti en Excel: {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la conversion en Excel {file_path}: {str(e)}")
            raise
    
    def to_sql_server(
        self,
        df: pd.DataFrame,
        table_name: str,
        connection_string: str,
        schema: str = 'dbo',
        if_exists: str = 'fail',
        **kwargs
    ) -> None:
        """
        Sauvegarde un DataFrame dans SQL Server.
        
        Args:
            df: DataFrame à sauvegarder
            table_name: Nom de la table
            connection_string: Chaîne de connexion SQL Server
            schema: Schéma de la base de données
            if_exists: Comportement si la table existe ('fail', 'replace', 'append')
            **kwargs: Arguments additionnels pour df.to_sql
        """
        try:
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
            df.to_sql(
                table_name,
                engine,
                schema=schema,
                if_exists=if_exists,
                index=False,
                **kwargs
            )
            logger.info(f"DataFrame sauvegardé dans SQL Server: {table_name}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde dans SQL Server: {str(e)}")
            raise
    
    def to_sqlite(
        self,
        df: pd.DataFrame,
        table_name: str,
        db_path: Union[str, Path],
        if_exists: str = 'fail',
        **kwargs
    ) -> None:
        """
        Sauvegarde un DataFrame dans SQLite.
        
        Args:
            df: DataFrame à sauvegarder
            table_name: Nom de la table
            db_path: Chemin de la base SQLite
            if_exists: Comportement si la table existe ('fail', 'replace', 'append')
            **kwargs: Arguments additionnels pour df.to_sql
        """
        try:
            engine = create_engine(f"sqlite:///{db_path}")
            df.to_sql(
                table_name,
                engine,
                if_exists=if_exists,
                index=False,
                **kwargs
            )
            logger.info(f"DataFrame sauvegardé dans SQLite: {table_name}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde dans SQLite: {str(e)}")
            raise
    
    @staticmethod
    def validate_csv(file_path: Union[str, Path], required_columns: List[str]) -> bool:
        """
        Valide un fichier CSV.
        
        Args:
            file_path: Chemin du fichier
            required_columns: Colonnes requises
            
        Returns:
            bool: True si le CSV est valide
        """
        try:
            df = pd.read_csv(file_path)
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                logger.warning(f"Colonnes manquantes dans le CSV: {missing_columns}")
                return False
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la validation du CSV: {str(e)}")
            return False 