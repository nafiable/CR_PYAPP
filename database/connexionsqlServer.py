"""
Module de connexion à la base de données SQL Server.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

class SQLServerConnection:
    """Classe pour gérer la connexion à SQL Server."""
    
    def __init__(self, database_url: str = "mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"):
        """
        Initialise la connexion SQL Server.
        
        Args:
            database_url (str): URL de connexion SQL Server
        """
        self.database_url = database_url
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _create_engine(self) -> Engine:
        """
        Crée le moteur SQLAlchemy.
        
        Returns:
            Engine: Moteur SQLAlchemy
        """
        try:
            engine = create_engine(
                self.database_url,
                echo=False  # Set to True for debugging
            )
            logger.info(f"Moteur SQL Server créé: {self.database_url}")
            return engine
        except Exception as e:
            logger.error(f"Erreur lors de la création du moteur SQL Server: {str(e)}")
            raise
    
    def get_session(self):
        """
        Retourne une nouvelle session de base de données.
        
        Returns:
            Session: Session SQLAlchemy
        """
        try:
            session = self.SessionLocal()
            logger.debug("Nouvelle session SQL Server créée")
            return session
        except Exception as e:
            logger.error(f"Erreur lors de la création de la session SQL Server: {str(e)}")
            raise
    
    def get_connection(self):
        """
        Retourne une connexion à la base de données.
        
        Returns:
            Connection: Connexion SQLAlchemy
        """
        try:
            conn = self.engine.connect()
            logger.debug("Nouvelle connexion SQL Server créée")
            return conn
        except Exception as e:
            logger.error(f"Erreur lors de la création de la connexion SQL Server: {str(e)}")
            raise
