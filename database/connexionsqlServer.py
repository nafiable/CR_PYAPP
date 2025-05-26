import logging
import sqlalchemy
import pyodbc  # ou un autre driver comme pymssql
import urllib

from constantes.const1 import Constantes, load_config

logger = logging.getLogger(__name__)

class SQLServerConnection:
    """
    Classe pour gérer la connexion à une base de données SQL Server.
    """

    def __init__(self):
        """
        Initialise la classe avec les paramètres de connexion.

        """
        # Charger les constantes si ce n'est pas déjà fait
        load_config()
 # Utiliser les constantes chargées
        self.server = Constantes.BD_SERVER
        self.database = Constantes.BD_NAME
        self.user = Constantes.BD_USER
        self.password = Constantes.BD_PASSWORD

        # Vérifier que les constantes nécessaires sont chargées
        if not all([self.server, self.database, self.user, self.password]):
            logger.error("Les paramètres de connexion SQL Server ne sont pas correctement configurés dans config.env")

        # Encoder les paramètres de connexion pour l'URL SQLAlchemy
        params = urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password}')

        self.connection = None
        self.engine = None

    def open_connection(self):
        """
        Ouvre la connexion à la base de données SQL Server.
        """
 try:
            # Créer l'engine de connexion SQLAlchemy
            self.engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={params}')
 except Exception as e: # Gérer les exceptions lors de la connexion
            logger.error(f"Erreur lors de l'ouverture de la connexion SQL Server : {e}", exc_info=True)

    def close_connection(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.engine = None

    def get_engine(self):
        """
        Retourne l'engine de connexion SQLAlchemy.

        Returns:
            sqlalchemy.engine.base.Engine: L'engine de connexion SQLAlchemy.
        """
        # Retourner l'engine existant ou en créer un si nécessaire
        if not self.engine:
            self.open_connection()
 if not self.engine:
 # Gérer le cas où open_connection a échoué
 return None
        return self.engine
