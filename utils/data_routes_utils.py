"""
Fonctions utilitaires pour la gestion des données (tables, import/export, synchronisation).
Déplacées depuis data_routes.py pour réutilisation dans le dispatcher ou ailleurs.
"""

import pandas as pd
from pathlib import Path
from database.connexionsqlServer import SQLServerConnection
from database.connexionsqlLiter import SQLiteConnection
from utils.csv import CSVUtils
from utils.excel import ExcelUtils
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)


def get_tables_sqlite(db_path: str) -> list:
    """
    Récupère la liste des tables SQLite.
    Args:
        db_path (str): Chemin de la base SQLite
    Returns:
        list: Liste des noms de tables
    """
    sqlite_conn = SQLiteConnection(db_path)
    with sqlite_conn.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
    return tables


def get_table_data_sqlite(db_path: str, table: str) -> pd.DataFrame:
    """
    Récupère les données d'une table SQLite sous forme de DataFrame.
    Args:
        db_path (str): Chemin de la base SQLite
        table (str): Nom de la table
    Returns:
        pd.DataFrame: Données de la table
    """
    sqlite_conn = SQLiteConnection(db_path)
    with sqlite_conn.get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    return df


def import_csv_to_sqlite(csv_path: str, table: str, db_path: str, if_exists: str = 'append'):
    """
    Importe un fichier CSV dans une table SQLite.
    Args:
        csv_path (str): Chemin du fichier CSV
        table (str): Nom de la table
        db_path (str): Chemin de la base SQLite
        if_exists (str): 'append' ou 'replace'
    """
    df = CSVUtils.load_csv_to_dataframe(csv_path)
    engine = create_engine(f"sqlite:///{db_path}")
    CSVUtils.csv_to_sql(df, table, engine, if_exists=if_exists)


def import_excel_to_sqlite(excel_path: str, table: str, db_path: str, if_exists: str = 'append'):
    """
    Importe un fichier Excel dans une table SQLite.
    Args:
        excel_path (str): Chemin du fichier Excel
        table (str): Nom de la table
        db_path (str): Chemin de la base SQLite
        if_exists (str): 'append' ou 'replace'
    """
    df = ExcelUtils.load_excel_to_dataframe(excel_path)
    engine = create_engine(f"sqlite:///{db_path}")
    ExcelUtils.excel_to_sql(df, table, engine, if_exists=if_exists)


def export_table_to_csv_sqlite(table: str, db_path: str, output_path: str):
    """
    Exporte une table SQLite en CSV.
    Args:
        table (str): Nom de la table
        db_path (str): Chemin de la base SQLite
        output_path (str): Chemin du fichier CSV de sortie
    """
    sqlite_conn = SQLiteConnection(db_path)
    with sqlite_conn.get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    CSVUtils.write_dataframe_to_csv(df, output_path)


def export_table_to_excel_sqlite(table: str, db_path: str, output_path: str):
    """
    Exporte une table SQLite en Excel.
    Args:
        table (str): Nom de la table
        db_path (str): Chemin de la base SQLite
        output_path (str): Chemin du fichier Excel de sortie
    """
    sqlite_conn = SQLiteConnection(db_path)
    with sqlite_conn.get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    ExcelUtils.write_dataframe_to_excel(df, output_path, sheet_name="Sheet1")


def sync_table_sqlite_to_sqlserver(table: str, sqlite_db_path: str, sqlserver_conn_str: str):
    """
    Synchronise une table SQLite vers SQL Server.
    Args:
        table (str): Nom de la table
        sqlite_db_path (str): Chemin de la base SQLite
        sqlserver_conn_str (str): Chaîne de connexion SQL Server
    """
    sqlite_conn = SQLiteConnection(sqlite_db_path)
    with sqlite_conn.get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
    engine = create_engine(sqlserver_conn_str)
    CSVUtils.csv_to_sql(df, table, engine, if_exists='replace') 