import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from constantes.const1 import Constants, load_config

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
        print(f"Initialisation de la connexion SQLite avec le chemin : {self.db_path}") # Pour le débogage

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
                print(f"Erreur lors de la création de l'engine SQLite : {e}") # Pour le débogage
                self.engine = None # S'assurer que l'engine est None en cas d'erreur
        return self.engine
