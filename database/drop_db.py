"""
Script pour supprimer la base de données.
"""

import logging
import os

logger = logging.getLogger(__name__)

def drop_database():
    """Supprime la base de données SQLite."""
    try:
        if os.path.exists("database.db"):
            os.remove("database.db")
            logger.info("Base de données supprimée avec succès")
        else:
            logger.info("Base de données inexistante")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la base de données: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    drop_database() 