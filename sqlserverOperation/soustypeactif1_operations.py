# sqlserverOperation/soustypeactif1_operations.py

from sqlalchemy.engine import Connection

from sqlalchemy import text
from schemas.SousTypeActif1 import SousTypeActif1 as SousTypeActif1Schema
from typing import Dict, Any

# Définir le nom de la table pour plus de clarté
TABLE_NAME = "SousTypeActif1"

def create_soustypeactif1(connection: Connection, soustypeactif1_data: SousTypeActif1Schema) -> Dict[str, Any]:
    """
    Crée un nouvel enregistrement dans la table SousTypeActif1.

    Args:    connection: L'objet connexion SQLAlchemy.
        soustypeactif1_data: Les données de SousTypeActif1 à créer, sous forme de schéma Pydantic.

    Returns:
        Un dictionnaire représentant les données créées ou un message d'erreur.
    """
    try:
        # Construire la requête SQL d'insertion
        query = text(f"""
            INSERT INTO {TABLE_NAME} (id, idTypeAcif1, nom)
            VALUES (:id, :idTypeAcif1, :nom)
        """)
        connection.execute(query, soustypeactif1_data.model_dump())
        connection.commit()
        return {"status": "success", "message": "SousTypeActif1 créé avec succès", "data": soustypeactif1_data.model_dump()}
    except Exception as e:
        connection.rollback()
        return {"status": "error", "message": f"Erreur lors de la création de SousTypeActif1: {e}"}

def get_soustypeactif1_by_id(connection: Connection, soustypeactif1_id: int) -> Dict[str, Any]:
    """
    Récupère un enregistrement de la table SousTypeActif1 par son ID.

    Args:    connection: L'objet connexion SQLAlchemy.
        soustypeactif1_id: L'ID de SousTypeActif1 à récupérer.

    Returns:
        Un dictionnaire représentant les données de SousTypeActif1 ou None si non trouvé.
    """
    try:
        query = text(f"SELECT id, idTypeAcif1, nom FROM {TABLE_NAME} WHERE id = :id")
        result = connection.execute(query, {"id": soustypeactif1_id}).fetchone()
        if result:
            # Convertir le résultat en dictionnaire
            return dict(result)
        return None
    except Exception as e:
        return {"status": "error", "message": f"Erreur lors de la récupération de SousTypeActif1: {e}"}

def update_soustypeactif1(connection: Connection, soustypeactif1_id: int, soustypeactif1_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Met à jour un enregistrement existant dans la table SousTypeActif1.

    Args:
        connection: L'objet session SQLAlchemy pour la connexion à la base de données.
        soustypeactif1_id: L'ID de SousTypeActif1 à mettre à jour.
        soustypeactif1_data: Les données de SousTypeActif1 à mettre à jour, sous forme de dictionnaire.

    Returns:
        Un dictionnaire indiquant le statut de l'opération.
    """
    try:
        # Construire la requête SQL de mise à jour dynamiquement
        update_fields = ", ".join([f"[{key}] = :{key}" for key in soustypeactif1_data.keys()]) # Utiliser des crochets pour les noms de colonnes
        query = text(f"""
            UPDATE {TABLE_NAME}
            SET {update_fields}
            WHERE id = :id
        """)
        # Ajouter l'ID à mettre à jour aux données
        update_data = soustypeactif1_data.copy()
        update_data["id"] = soustypeactif1_id

        result = connection.execute(query, update_data)
        connection.commit()

        if result.rowcount > 0:
            return {"status": "success", "message": f"SousTypeActif1 avec ID {soustypeactif1_id} mis à jour avec succès"}
        else:
            return {"status": "info", "message": f"Aucun SousTypeActif1 trouvé avec l'ID {soustypeactif1_id} pour la mise à jour"}
    except Exception as e:
        connection.rollback()
        return {"status": "error", "message": f"Erreur lors de la mise à jour de SousTypeActif1: {e}"}

def delete_soustypeactif1(connection: Connection, soustypeactif1_id: int) -> Dict[str, Any]:
    """
    Supprime un enregistrement de la table SousTypeActif1 par son ID.

    Args:    connection: L'objet connexion SQLAlchemy.
        soustypeactif1_id: L'ID de SousTypeActif1 à supprimer.

    Returns:
        Un dictionnaire indiquant le statut de l'opération.
    """
    try:
        query = text(f"DELETE FROM {TABLE_NAME} WHERE id = :id")
        result = connection.execute(query, {"id": soustypeactif1_id})
        connection.commit()

        if result.rowcount > 0:
            return {"status": "success", "message": f"SousTypeActif1 avec ID {soustypeactif1_id} supprimé avec succès"}
        else:
            return {"status": "info", "message": f"Aucun SousTypeActif1 trouvé avec l'ID {soustypeactif1_id} pour la suppression"}
    except Exception as e:
        connection.rollback()
        return {"status": "error", "message": f"Erreur lors de la suppression de SousTypeActif1: {e}"}