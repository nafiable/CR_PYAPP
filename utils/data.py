# -*- coding: utf-8 -*-

import pandas as pd
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

class DataUtils:
    """
    Classe utilitaire pour les opérations sur les données et l'interaction avec la base de données.
    """

    @staticmethod
    def load_dataframe_to_sql(dataframe: pd.DataFrame, tablename: str, connection, if_exists: str = 'fail'):
        """
        Charge un DataFrame pandas dans une table SQL.

        Args:
            dataframe (pd.DataFrame): Le DataFrame à charger.
            tablename (str): Le nom de la table SQL cible.
            connection: L'objet de connexion à la base de données (SQLAlchemy engine ou connexion).
            if_exists (str): Comment se comporter si la table existe déjà ('fail', 'replace', 'append').
                             Par défaut 'fail'.
        """
        try:
            dataframe.to_sql(name=tablename, con=connection, if_exists=if_exists, index=False)
            logger.info(f"DataFrame chargé dans la table '{tablename}' avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du DataFrame dans la table '{tablename}': {e}")
            raise

    @staticmethod
    def load_dict_to_sql(data: list[dict], tablename: str, connection):
        """
        Charge une liste de dictionnaires dans une table SQL.

        Args:
            data (list[dict]): La liste de dictionnaires à charger.
            tablename (str): Le nom de la table SQL cible.
            connection: L'objet de connexion à la base de données (SQLAlchemy engine ou connexion).
        """
        try:
            df = pd.DataFrame(data)
            DataUtils.load_dataframe_to_sql(df, tablename, connection, if_exists='append') # Utilise 'append' par défaut pour les dictionnaires
            logger.info(f"Dictionnaires chargés dans la table '{tablename}' avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des dictionnaires dans la table '{tablename}': {e}")
            raise

    @staticmethod
    def load_sql_to_dataframe(query: str, connection) -> pd.DataFrame:
        """
        Charge les résultats d'une requête SQL dans un DataFrame pandas.

        Args:
            query (str): La requête SQL à exécuter.
            connection: L'objet de connexion à la base de données (SQLAlchemy engine ou connexion).

        Returns:
            pd.DataFrame: Le DataFrame contenant les résultats de la requête.
        """
        try:
            df = pd.read_sql(query, con=connection)
            logger.info("Données chargées depuis la base de données vers un DataFrame avec succès.")
            return df
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données SQL vers un DataFrame: {e}")
            raise

    @staticmethod
    def load_sql_to_dict(query: str, connection) -> list[dict]:
        """
        Charge les résultats d'une requête SQL en liste de dictionnaires.

        Args:
            query (str): La requête SQL à exécuter.
            connection: L'objet de connexion à la base de données (SQLAlchemy engine ou connexion).

        Returns:
            list[dict]: La liste de dictionnaires contenant les résultats.
        """
        try:
            with connection.connect() as conn:
                result = conn.execute(text(query))
                # Convertir les résultats en liste de dictionnaires
                # Les noms de colonnes sont dans result.keys()
                rows_as_dict = [dict(zip(result.keys(), row)) for row in result]
            logger.info("Données chargées depuis la base de données vers une liste de dictionnaires avec succès.")
            return rows_as_dict
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données SQL vers une liste de dictionnaires: {e}")
            raise
