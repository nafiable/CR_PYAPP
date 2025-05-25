# -*- coding: utf-8 -*-

"""
    Module pour les opérations CRUD sur l'entité SousTypeActif1 dans SQLite.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.SousTypeActif1 import SousTypeActif1Create, SousTypeActif1Update

def create_soustypeactif1(connection: Session, soustypeactif1_data: SousTypeActif1Create):
    """
    Crée un nouveau SousTypeActif1 dans la base de données SQLite.

    Args:
        connection: La session SQLAlchemy pour la connexion à la base de données.
        soustypeactif1_data: Les données du SousTypeActif1 à créer (modèle Pydantic).

    Returns:
        Le SousTypeActif1 créé sous forme de dictionnaire, ou None en cas d'échec.
    """
    try:
        # Construction de la requête d'insertion
        query = text(
            INSERT INTO SousTypeActif1 (id, idTypeAcif1, nom)
            VALUES (:id, :idTypeAcif1, :nom)
        """)
        connection.execute(query, soustypeactif1_data.dict())
        connection.commit()
        # Pour SQLite, on peut ne pas récupérer l'objet inséré directement sans un SELECT
        # On retourne simplement les données fournies pour confirmation
        return soustypeactif1_data.dict()
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la création du SousTypeActif1 : {e}")
        return None

def get_soustypeactif1_by_id(connection: Session, soustypeactif1_id: int):
    """
    Récupère un SousTypeActif1 par son ID depuis la base de données SQLite.

    Args:
        connection: La session SQLAlchemy pour la connexion à la base de données.
        soustypeactif1_id: L'ID du SousTypeActif1 à récupérer.

    Returns:
        Le SousTypeActif1 trouvé sous forme de dictionnaire, ou None s'il n'existe pas.
    """
    try:
        query = text("""
            SELECT id, idTypeAcif1, nom
            FROM SousTypeActif1
            WHERE id = :id
        """)
        result = connection.execute(query, {"id": soustypeactif1_id}).fetchone()
        if result:
            return dict(result)
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération du SousTypeActif1 : {e}")
        return None # Retourner None si une erreur se produit

def update_soustypeactif1(connection: Session, soustypeactif1_id: int, soustypeactif1_data: SousTypeActif1Update):
    """
    Met à jour un SousTypeActif1 existant dans la base de données SQLite.

    Args:
        connection: La session SQLAlchemy pour la connexion à la base de données.
        soustypeactif1_id: L'ID du SousTypeActif1 à mettre à jour.
        soustypeactif1_data: Les données de mise à jour (modèle Pydantic).

    Returns:
        Le SousTypeActif1 mis à jour sous forme de dictionnaire, ou None en cas d'échec.
    """
    try:
        # Préparation des données à mettre à jour
        update_values = soustypeactif1_data.dict(exclude_unset=True)
        if not update_values:
            return get_soustypeactif1_by_id(connection, soustypeactif1_id) # Aucune mise à jour à faire

        # Construction de la requête de mise à jour
        # Note : Une approche plus robuste construirait dynamiquement la clause SET
        # pour gérer uniquement les champs présents dans update_values.
        # Pour simplifier ici, on suppose que soustypeactif1_data contient tous les champs
        query = text(
            UPDATE SousTypeActif1
            SET idTypeAcif1 = :idTypeAcif1, nom = :nom
            WHERE id = :id
        """)
        result = connection.execute(query, {**update_values, "id": soustypeactif1_id})
        connection.commit()
        if result.rowcount > 0:
            return get_soustypeactif1_by_id(connection, soustypeactif1_id)
        return None # Aucun SousTypeActif1 trouvé avec cet ID
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la mise à jour du SousTypeActif1 : {e}")
        return None

def delete_soustypeactif1(connection: Session, soustypeactif1_id: int):
    """
    Supprime un SousTypeActif1 par son ID depuis la base de données SQLite.

    Args:
        connection: La session SQLAlchemy pour la connexion à la base de données.
        soustypeactif1_id: L'ID du SousTypeActif1 à supprimer.

    Returns:
        True si la suppression a réussi, False sinon.
    """
    try:
        query = text("""
            DELETE FROM SousTypeActif1 # Requête de suppression
            WHERE id = :id
        """)
        result = connection.execute(query, {"id": soustypeactif1_id})
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la suppression du SousTypeActif1 : {e}")
        return False