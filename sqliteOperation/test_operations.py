# sqliteOperation/test_operations.py

from database.connexionsqlLiter import SQLiteConnection
from sqlalchemy import text
import logging

# Configuration du logging (à affiner selon les besoins)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def insert_test_data(connection: SQLiteConnection, id: int, nom: str):
    """
    Insère une ligne de test dans la table TestTable de la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLite.
        id: L'ID à insérer.
        nom: Le nom à insérer.
    """
    try:
        # Obtient l'engine de connexion
        engine = connection.get_engine()
        
        # Ouvre une connexion
        with engine.connect() as conn:
            # Définir la requête d'insertion
            query = text("INSERT INTO TestTable (id, nom) VALUES (:id, :nom)")
            
            # Exécuter la requête avec les paramètres
            conn.execute(query, {"id": id, "nom": nom})
            
            # Committer la transaction
            conn.commit()
            
            logging.info(f"Données insérées dans TestTable (SQLite): ID={id}, Nom={nom}")
            
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion dans TestTable (SQLite): {e}")
        # Gérer l'erreur (lever une exception, retourner False, etc.)
        raise

if __name__ == '__main__':
    # Exemple d'utilisation (pour les tests locaux)
    # Assurez-vous que le fichier config.env est configuré et que la table TestTable existe
    from constantes.const1 import load_config, CONSTANTS
    
    load_config()
    
    sqlite_connection = None
    try:
        sqlite_connection = SQLiteConnection()
        
        # Insérer quelques données de test
        insert_test_data(sqlite_connection, 1, "Test SQLite 1")
        insert_test_data(sqlite_connection, 2, "Test SQLite 2")
        
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution de l'exemple : {e}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close_connection()