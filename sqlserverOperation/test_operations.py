# sqlserverOperation/test_operations.py

from database.connexionsqlServer import SQLServerConnection
from sqlalchemy.orm import Session
from sqlalchemy import text

def insert_test_data(conn: SQLServerConnection, id: int, name: str):
    """
    Insère une ligne de données de test dans la table TestTable.

    Args:
        conn (SQLServerConnection): L'objet de connexion SQL Server.
        id (int): L'ID de la ligne à insérer.
        name (str): Le nom de la ligne à insérer.
    """
    # Obtenir l'engine de connexion
    engine = conn.get_engine()

    # Utiliser une session pour l'opération d'insertion
    with Session(engine) as session:
        try:
            # Définir la requête d'insertion
            insert_query = text("INSERT INTO TestTable (id, name) VALUES (:id, :name)")

            # Exécuter la requête avec les paramètres
            session.execute(insert_query, {"id": id, "name": name})

            # Committer la transaction
            session.commit()
            print(f"Données insérées avec succès : ID={id}, Nom='{name}'")

        except Exception as e:
            session.rollback()
            print(f"Erreur lors de l'insertion des données : {e}")

if __name__ == '__main__':
    # Exemple d'utilisation (pour les tests locaux)
    # Assurez-vous que config.env est configuré et que la fonction load_config a été appelée
    # depuis un point d'entrée approprié avant d'exécuter ce script directement.
    # Exemple fictif :
    # from constantes.const1 import load_config, CONSTANTS
    # load_config()
    #
    # try:
    #     sql_conn = SQLServerConnection()
    #     insert_test_data(sql_conn, 1, "Test Data 1")
    #     insert_test_data(sql_conn, 2, "Test Data 2")
    # finally:
    #     # La connexion devrait idéalement être gérée dans un contexte plus large de l'application
    #     pass # Pas besoin de fermer explicitement l'engine SQLAlchemy ici