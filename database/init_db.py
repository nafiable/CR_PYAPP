"""
Script d'initialisation de la base de données.
"""

import logging
from database.connexionsqlLiter import SQLiteConnection
from database.models import Base

logger = logging.getLogger(__name__)

def init_database():
    """Initialise la base de données en créant toutes les tables."""
    try:
        # Création de la connexion
        connection = SQLiteConnection()
        
        # Création des tables
        Base.metadata.create_all(connection.engine)
        
        logger.info("Base de données initialisée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_database() 