import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from constantes.const1 import Constants, load_config
import logging

logger = logging.getLogger(__name__)
class SQLiteConnection:
    """
    Gère la connexion à une base de données SQLite.
    """

    def __init__(self):
        """
        Initialise la connexion SQLite en utilisant les constantes de configuration.
        """
        load_config() # Assurez-vous que les constantes sont chargées
        self.db_path = Constants.SQLITE_DB_PATH
        self.engine: Engine = None
        logger.info(f"Initialisation de la connexion SQLite avec le chemin : {self.db_path}") # Pour le débogage

    def open_connection(self):
        """
        Ouvre la connexion à la base de données SQLite et crée l'engine SQLAlchemy.
        Gère les erreurs de connexion.
        """
        """
        Ouvre la connexion à la base de données SQLite et crée l'engine SQLAlchemy.
        """
        self.connection = sqlite3.connect(self.db_path)
        self.engine = create_engine(f'sqlite:///{self.db_path}')

    def close_connection(self):
        """
        Ferme la connexion à la base de données SQLite.
        """
        """
        Ferme l'engine SQLAlchemy si elle est ouverte.
        """
        if self.connection:
            self.connection.close()

    def get_engine(self) -> Engine:
        """
        Retourne l'engine SQLAlchemy pour la base de données SQLite.

        Returns:
            Engine: L'engine SQLAlchemy.
        """
        if self.engine is None:
            try:
                self.engine = create_engine(f'sqlite:///{self.db_path}')
            except Exception as e:
                logger.error(f"Erreur lors de la création de l'engine SQLite : {e}") # Pour le débogage
                self.engine = None # S'assurer que l'engine est None en cas d'erreur
        return self.engine

def get_database_config(db_path: str) -> dict:
    """
    Récupère les valeurs de configuration de la table 'config' dans la base de données SQLite.

    Args:
        db_path: Le chemin vers le fichier de base de données SQLite.

    Returns:
        Un dictionnaire contenant les paires clé-valeur de la table config.
        Retourne un dictionnaire vide en cas d'erreur ou si la table est vide.
    """
    config_values = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # TODO: Implémenter la requête pour sélectionner les données de la table 'config'
        # Exemple: cursor.execute("SELECT variable, valeur FROM config")
        # TODO: Itérer sur les résultats et peupler le dictionnaire config_values
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la lecture de la table config : {e}")
    return config_values
