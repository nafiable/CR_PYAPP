"""
Module de connexion à la base de données SQLite.
"""

import logging
import sqlite3
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from constantes import const1

logger = logging.getLogger(__name__)

class SQLiteConnection:
    """Classe pour gérer la connexion à SQLite."""
    
    def __init__(self, database_url: str = "sqlite:///database.db"):
        """
        Initialise la connexion SQLite.
        
        Args:
            database_url (str): URL de connexion SQLite
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
                echo=False,  # Set to True for debugging
                connect_args={"check_same_thread": False}
            )
            logger.info(f"Moteur SQLite créé: {self.database_url}")
            return engine
        except Exception as e:
            logger.error(f"Erreur lors de la création du moteur SQLite: {str(e)}")
            raise
    
    def get_session(self):
        """
        Retourne une nouvelle session de base de données.
        
        Returns:
            Session: Session SQLAlchemy
        """
        try:
            session = self.SessionLocal()
            logger.debug("Nouvelle session SQLite créée")
            return session
        except Exception as e:
            logger.error(f"Erreur lors de la création de la session SQLite: {str(e)}")
            raise
    
    def get_connection(self):
        """
        Retourne une connexion à la base de données.
        
        Returns:
            Connection: Connexion SQLAlchemy
        """
        try:
            conn = self.engine.connect()
            logger.debug("Nouvelle connexion SQLite créée")
            return conn
        except Exception as e:
            logger.error(f"Erreur lors de la création de la connexion SQLite: {str(e)}")
            raise
    
    @contextmanager
    def get_session_context(self) -> Generator[Session, None, None]:
        """
        Fournit un contexte de session SQLAlchemy.
        
        Yields:
            Session: Une session SQLAlchemy
            
        Example:
            with connection.get_session_context() as session:
                result = session.query(Model).all()
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erreur lors de la session SQLite: {str(e)}")
            raise
        finally:
            session.close()
    
    @contextmanager
    def get_connection_context(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Fournit une connexion SQLite directe.
        
        Yields:
            Connection: Une connexion SQLite
            
        Example:
            with connection.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        # Extrait le nom du fichier de l'URL
        db_name = self.database_url.split("///")[-1]
        conn = sqlite3.connect(db_name)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Erreur lors de la connexion SQLite: {str(e)}")
            raise
        finally:
            conn.close()
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à la base de données.
        
        Returns:
            bool: True si la connexion est établie, False sinon
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
            logger.info("Test de connexion SQLite réussi")
            return True
        except Exception as e:
            logger.error(f"Échec du test de connexion SQLite: {str(e)}")
            return False
    
    def init_database(self):
        """
        Initialise la base de données SQLite avec le schéma.
        
        Cette méthode lit le fichier sqliteCreation.sql et exécute
        les requêtes de création des tables.
        """
        try:
            with open("database/sqliteCreation.sql", "r", encoding="utf-8") as f:
                sql_script = f.read()
            
            with self.get_connection_context() as conn:
                conn.executescript(sql_script)
            
            logger.info("Base de données SQLite initialisée avec succès")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base SQLite: {str(e)}")
            return False

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
