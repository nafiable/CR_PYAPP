# -*- coding: utf-8 -*-

import csv
import pandas as pd
import logging
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

class CSVUtils:
    """
    Classe utilitaire pour les opérations sur les fichiers CSV et les interactions avec SQL/Excel.
    """

    @staticmethod
    def load_csv_to_dict(filepath: str) -> List[dict]:
        """
        Charge un fichier CSV et retourne une liste de dictionnaires.
        """
        data = []
        logger.info(f"Loading CSV file: {filepath}")
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        logger.info(f"Successfully loaded {len(data)} rows from {filepath}")
        return data

    @staticmethod
    def load_csv_to_dataframe(filepath: str, encoding: str = 'utf-8', sep: str = ',', **kwargs) -> pd.DataFrame:
        """
        Charge un fichier CSV et retourne un DataFrame pandas.
        """
        logger.info(f"Loading CSV file into DataFrame: {filepath}")
        return pd.read_csv(filepath, encoding=encoding, sep=sep, **kwargs)

    @staticmethod
    def write_dict_to_csv(data: List[dict], filepath: str):
        """
        Écrit une liste de dictionnaires dans un fichier CSV.
        """
        if not data:
            logger.warning(f"No data to write to CSV file: {filepath}")
            return
        logger.info(f"Writing {len(data)} dictionaries to CSV file: {filepath}")
        keys = data[0].keys()
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Successfully wrote data to CSV file: {filepath}")

    @staticmethod
    def write_dataframe_to_csv(dataframe: pd.DataFrame, filepath: str, encoding: str = 'utf-8', sep: str = ',', **kwargs):
        """
        Écrit un DataFrame pandas dans un fichier CSV.
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(filepath, index=False, encoding=encoding, sep=sep, **kwargs)
        logger.info(f"DataFrame sauvegardé en CSV: {filepath}")

    @staticmethod
    def csv_to_excel(csv_path: str, excel_path: str, encoding: str = 'utf-8', sep: str = ',', **kwargs):
        """
        Convertit un fichier CSV en fichier Excel.
        """
        df = CSVUtils.load_csv_to_dataframe(csv_path, encoding=encoding, sep=sep, **kwargs)
        df.to_excel(excel_path, index=False)
        logger.info(f"CSV converti en Excel : {excel_path}")

    @staticmethod
    def csv_to_sql(df: pd.DataFrame, table_name: str, connection: Engine, if_exists: str = 'fail', **kwargs):
        """
        Importe un DataFrame (issu d'un CSV) dans une table SQL.
        """
        df.to_sql(table_name, connection, if_exists=if_exists, index=False, **kwargs)
        logger.info(f"DataFrame importé dans SQL : {table_name}")

    @staticmethod
    def csv_file_to_sql(csv_path: str, table_name: str, connection: Engine, encoding: str = 'utf-8', sep: str = ',', if_exists: str = 'fail', **kwargs):
        """
        Importe un fichier CSV dans une table SQL.
        """
        df = CSVUtils.load_csv_to_dataframe(csv_path, encoding=encoding, sep=sep, **kwargs)
        CSVUtils.csv_to_sql(df, table_name, connection, if_exists=if_exists, **kwargs)

    @staticmethod
    def sql_to_csv(query: str, csv_path: str, connection: Engine, encoding: str = 'utf-8', sep: str = ',', **kwargs):
        """
        Exporte le résultat d'une requête SQL vers un fichier CSV.
        """
        df = pd.read_sql_query(query, connection)
        CSVUtils.write_dataframe_to_csv(df, csv_path, encoding=encoding, sep=sep, **kwargs)
        logger.info(f"Données SQL exportées en CSV : {csv_path}")

    @staticmethod
    def validate_csv(file_path: Union[str, Path], required_columns: List[str], encoding: str = 'utf-8', sep: str = ',') -> bool:
        """
        Valide qu'un fichier CSV contient bien toutes les colonnes requises.
        """
        try:
            df = pd.read_csv(file_path, encoding=encoding, sep=sep)
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                logger.warning(f"Colonnes manquantes dans le CSV: {missing_columns}")
                return False
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la validation du CSV: {str(e)}")
            return False
