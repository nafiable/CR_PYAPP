# sqliteOperation/sousclassif1_operations.py

import logging
from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger(__name__)

def create_sousclassif1(connection: Session, sousclassif1_data: dict):
    """
    Crée une nouvelle entrée dans la table SousClassif1.

    Args:
        connection: L'objet de connexion SQLAlchemy à la base de données SQLite.
        sousclassif1_data: Un dictionnaire contenant les données de la sous-classification 1.

    Returns:
        Le résultat de l'insertion.
    """
    try:
        # Exemple d'insertion. Adapter la requête SQL en fonction des champs réels de la table.
        query = text("INSERT INTO SousClassif1 (id, idClassif1, nom) VALUES (:id, :idClassif1, :nom);")
        result = connection.execute(query, sousclassif1_data)
        logger.info(f"Attempting to create SousClassif1 with data: {sousclassif1_data}")
        connection.commit()
        logger.info("SousClassif1 created successfully.")
        return {"status": "success", "message": "SousClassif1 créé avec succès."}
    except Exception as e:
        connection.rollback()
        logger.error(f"Error creating SousClassif1: {e}")
        return {"status": "error", "message": f"Erreur lors de la création de SousClassif1 : {e}"}

def get_sousclassif1_by_id(connection: Session, sousclassif1_id: int):
    """
    Récupère une entrée de la table SousClassif1 par son ID.

    Args:
        connection: L'objet de connexion SQLAlchemy à la base de données SQLite.
        sousclassif1_id: L'ID de la sous-classification 1 à récupérer.

    Returns:
        Un dictionnaire représentant la sous-classification 1 ou None si non trouvé.
    """
    try:
        query = text("SELECT id, idClassif1, nom FROM SousClassif1 WHERE id = :id;")
        logger.info(f"Attempting to get SousClassif1 with ID: {sousclassif1_id}")
        result = connection.execute(query, {"id": sousclassif1_id}).fetchone()
        if result:
            logger.info(f"SousClassif1 found with ID: {sousclassif1_id}")
            return {"status": "success", "data": dict(result)}
        else:
            logger.info(f"SousClassif1 not found with ID: {sousclassif1_id}")
            return {"status": "success", "data": None, "message": "SousClassif1 non trouvé."}
    except Exception as e:
        logger.error(f"Error getting SousClassif1 with ID {sousclassif1_id}: {e}")
        return {"status": "error", "message": f"Erreur lors de la récupération de SousClassif1 : {e}"}

def update_sousclassif1(connection: Session, sousclassif1_id: int, sousclassif1_data: dict):
    """
    Met à jour une entrée existante dans la table SousClassif1.

    Args:
        connection: L'objet de connexion SQLAlchemy à la base de données SQLite.
        sousclassif1_id: L'ID de la sous-classification 1 à mettre à jour.
        sousclassif1_data: Un dictionnaire contenant les données de mise à jour.

    Returns:
        Le résultat de la mise à jour.
    """
    try:
        # Adapter la requête SQL en fonction des champs à mettre à jour.
        # Cet exemple suppose qu'on peut mettre à jour le nom et l'idClassif1.
        query = text("UPDATE SousClassif1 SET idClassif1 = :idClassif1, nom = :nom WHERE id = :id")
        result = connection.execute(query, {"id": sousclassif1_id, **sousclassif1_data})
        logger.info(f"Attempting to update SousClassif1 with ID {sousclassif1_id} and data: {sousclassif1_data}")
        connection.commit()
        if result.rowcount > 0:
            logger.info(f"SousClassif1 with ID {sousclassif1_id} updated successfully.")
            return {"status": "success", "message": "SousClassif1 mis à jour avec succès."}
        else:
            logger.warning(f"SousClassif1 with ID {sousclassif1_id} not found for update.")
            return {"status": "success", "message": "SousClassif1 non trouvé pour mise à jour."}
    except Exception as e:
        connection.rollback()
        logger.error(f"Error updating SousClassif1 with ID {sousclassif1_id}: {e}")
        return {"status": "error", "message": f"Erreur lors de la mise à jour de SousClassif1 : {e}"}

def delete_sousclassif1(connection: Session, sousclassif1_id: int):
    """
    Supprime une entrée de la table SousClassif1 par son ID.

    Args:
        connection: L'objet de connexion SQLAlchemy à la base de données SQLite.
        sousclassif1_id: L'ID de la sous-classification 1 à supprimer.

    Returns:
        Le résultat de la suppression.
    """
    try:
        query = text("DELETE FROM SousClassif1 WHERE id = :id")
        logger.info(f"Attempting to delete SousClassif1 with ID: {sousclassif1_id}")
        result = connection.execute(query, {"id": sousclassif1_id});
        connection.commit()
        if result.rowcount > 0:
            logger.info(f"SousClassif1 with ID {sousclassif1_id} deleted successfully.")
            return {"status": "success", "message": "SousClassif1 supprimé avec succès."}
        else:
            logger.warning(f"SousClassif1 with ID {sousclassif1_id} not found for deletion.")
            return {"status": "success", "message": "SousClassif1 non trouvé pour suppression."}
    except Exception as e:
        connection.rollback()
        logger.error(f"Error deleting SousClassif1 with ID {sousclassif1_id}: {e}")
        return {"status": "error", "message": f"Erreur lors de la suppression de SousClassif1 : {e}"}