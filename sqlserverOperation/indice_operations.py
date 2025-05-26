# sqlserverOperation/indice_operations.py

# sqlserverOperation/indice_operations.py

from sqlalchemy.orm import Session
from sqlalchemy import text, insert, select, update, delete
import logging

# Assurez-vous que votre objet de connexion ou votre session SQLAlchemy est passé ici
# Exemple: from database.connexionsqlServer import SQLServerConnection

# Vous pourriez définir ici une représentation de la table 'Indice' si vous utilisez SQLAlchemy Core de manière plus structurée
def create_indice(connection: Session, indice_data: dict):
    """
logger = logging.getLogger(__name__)
    """
    Insère un nouvel indice dans la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données.
        indice_data: Dictionnaire contenant les données de l'indice (par ex. {'id': 1, 'nom': 'Mon Indice'}).

    Returns:
        Le nouvel indice créé ou None si l'insertion échoue.
    """
    try:
        # Exemple d'insertion basique avec SQLAlchemy Core ou ORM
        query = insert(text("Indice")).values(indice_data)
        connection.execute(query, indice_data)
        connection.commit()
        logger.info(f"Indice créé avec succès : {indice_data.get('nom')}")
 conn.commit()
        # Pour des besoins simples, on peut retourner les données insérées
        return indice_data

    except Exception as e:
        connection.rollback()
        logger.error(f"Erreur lors de la création de l'indice : {e}")
        return None

def get_indice_by_id(connection: Session, indice_id: int):
    """
    Récupère un indice par son ID depuis la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données.
        indice_id: L'ID de l'indice à récupérer.

    Returns:
        Un dictionnaire représentant l'indice ou None s'il n'est pas trouvé.
    """
    try:
        # Exemple de sélection basique
 result = connection.execute(select(text("id, nom")).select_from(text("Indice")).where(text("id = :id")), {"id": indice_id}).fetchone()
        if result:
            # Convertir le résultat en dictionnaire
            return dict(result._mapping)
        return None
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'indice par ID {indice_id}: {e}")
        return None

def update_indice(connection: Session, indice_id: int, indice_data: dict):
    """
    Met à jour un indice existant dans la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données.
        indice_id: L'ID de l'indice à mettre à jour.
        indice_data: Dictionnaire contenant les données à mettre à jour (par ex. {'nom': 'Nouveau Nom'}).

    Returns:
        True si la mise à jour réussit, False sinon.
    """
    try:
        # Exemple de mise à jour basique
        # Assurez-vous que indice_data ne contient pas l'ID pour la clause SET
        update_values = {k: v for k, v in indice_data.items() if k != 'id'}
        if not update_values:
 logger.warning(f"Aucune donnée de mise à jour fournie pour l'indice ID {indice_id}.")
            return False

        parameters = {"id": indice_id, **update_values}

 query = update(text("Indice")).where(text("id = :id")).values(update_values)
        result = connection.execute(query, parameters)
        if result.rowcount > 0:
 logger.info(f"Indice ID {indice_id} mis à jour avec succès.")
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la mise à jour de l'indice : {e}")
        return False

def delete_indice(connection: Session, indice_id: int):
    """
    Supprime un indice par son ID de la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données.
        indice_id: L'ID de l'indice à supprimer.

    Returns:
        True si la suppression réussit, False sinon.
    """
    try:
        # Exemple de suppression basique
 query = delete(text("Indice")).where(text("id = :id"))
        result = connection.execute(query, {"id": indice_id})
        if result.rowcount > 0:
 logger.info(f"Indice ID {indice_id} supprimé avec succès.")
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la suppression de l'indice : {e}")
        return False