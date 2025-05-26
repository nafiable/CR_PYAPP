# sqlserverOperation/classif1_operations.py

# sqlserverOperation/classif1_operations.py

from sqlalchemy.orm import Session
from sqlalchemy import text
# Supposons que vous avez un modèle SQLAlchemy ou que vous utilisez directement les noms de tables
# from schemas.Classif1 import Classif1 as Classif1Schema # Exemple si vous avez des modèles SQLAlchemy
import logging

def create_classif1(connection: Session, classif1_data: dict):
    """
    Insère une nouvelle Classif1 dans la base de données SQL Server.

    Args:
        connection: L'objet session SQLAlchemy pour la connexion à la base de données.
        classif1_data: Un dictionnaire contenant les données de la Classif1 (par exemple, {'nom': 'Nouvelle Classification'}).
    """
    try:
        # Exemple d'insertion, adapter selon votre structure de table et si vous utilisez des modèles SQLAlchemy
        # Exemple d'insertion avec une requête texte si pas de modèles SQLAlchemy mappés
        # Assurez-vous que classif1_data est un dictionnaire avec une clé 'nom'
        query = text("INSERT INTO Classif1 (nom) VALUES (:nom)")
        result = connection.execute(query, classif1_data)
        connection.commit()
        return {"message": "Classif1 créée avec succès", "id": result.lastrowid}

    except Exception as e:
        connection.rollback()
        logging.error(f"Erreur lors de la création de la Classif1 : {e}")
        raise

def get_classif1_by_id(connection: Session, classif1_id: int):
    """
    Récupère une Classif1 par son ID depuis la base de données SQL Server.

    Args:
        connection: L'objet session SQLAlchemy.
        classif1_id: L'ID de la Classif1 à récupérer.

    Returns:
        Un dictionnaire représentant la Classif1 ou None si non trouvée.
    """
    try:
        # Exemple de sélection, adapter selon votre structure
        query = text("SELECT id, nom FROM Classif1 WHERE id = :classif1_id")
        result = connection.execute(query, {"classif1_id": classif1_id}).fetchone()

        if result:
            # Convertir le résultat en dictionnaire
            return dict(result)
        return None

    except Exception as e:
        logging.error(f"Erreur lors de la récupération de la Classif1 : {e}")
        raise

def update_classif1(connection: Session, classif1_id: int, classif1_data: dict):
    """
    Met à jour une Classif1 existante dans la base de données SQL Server.

    Args:
        connection: L'objet session SQLAlchemy.
        classif1_id: L'ID de la Classif1 à mettre à jour.
        classif1_data: Un dictionnaire contenant les données à mettre à jour (par exemple, {'nom': 'Classification Modifiée'}).

    Returns:
        Un dictionnaire représentant la Classif1 mise à jour ou None si non trouvée.
    """
    try:
        # Exemple de mise à jour, adapter selon votre structure
        query = text("UPDATE Classif1 SET nom = :nom WHERE id = :classif1_id")
        result = connection.execute(query, {"nom": classif1_data.get("nom"), "classif1_id": classif1_id})
        connection.commit()

        if result.rowcount > 0:
            # Récupérer et retourner la Classif1 mise à jour
            return get_classif1_by_id(connection, classif1_id)
        return None # Retourne None si aucun enregistrement n'a été mis à jour

    except Exception as e:
        connection.rollback()
        logging.error(f"Erreur lors de la mise à jour de la Classif1 : {e}")
        raise

def delete_classif1(connection: Session, classif1_id: int):
    """
    Supprime une Classif1 par son ID depuis la base de données SQL Server.

    Args:
        connection: L'objet session SQLAlchemy.
        classif1_id: L'ID de la Classif1 à supprimer.

    Returns:
        True si la suppression a réussi, False sinon.
    """
    try:
        # Exemple de suppression, adapter selon votre structure
        query = text("DELETE FROM Classif1 WHERE id = :classif1_id")
        result = connection.execute(query, {"classif1_id": classif1_id})
        connection.commit()

        return result.rowcount > 0

    except Exception as e:
        connection.rollback()
        logging.error(f"Erreur lors de la suppression de la Classif1 : {e}")
        raise