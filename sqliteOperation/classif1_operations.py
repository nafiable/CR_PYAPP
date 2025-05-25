# -*- coding: utf-8 -*-

"""
Module des opérations CRUD pour la table Classif1 dans la base de données SQLite.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from ..schemas.Classif1 import Classif1 as Classif1Schema

# Assurez-vous que les classes de connexion SQLite sont importées si nécessaire,
# ou que la fonction de connexion retourne un objet Session SQLAlchemy.
# Exemple :
# from ..database.connexionsqlLiter import SQLiteConnection

def create_classif1(connection: Session, classif1_data: Classif1Schema):
    """
    Crée une nouvelle entrée dans la table Classif1.

    Args:
        connection: La session de base de données SQLAlchemy.
        classif1_data: Les données de la Classif1 à créer (modèle Pydantic).

    Returns:
        Le modèle Pydantic de la Classif1 créée.
    """
    try:
        # Exemple d'insertion avec SQLAlchemy Core (peut être adapté pour l'ORM)
        query = text("INSERT INTO Classif1 (id, nom) VALUES (:id, :nom)")
        connection.execute(query, {"id": classif1_data.id, "nom": classif1_data.nom})
        connection.commit()
        return classif1_data
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la création de Classif1 : {e}")
        raise # Propage l'exception

def get_classif1_by_id(connection: Session, classif1_id: int):
    """
    Récupère une Classif1 par son ID.

    Args:
        connection: La session de base de données SQLAlchemy.
        classif1_id: L'ID de la Classif1 à récupérer.

    Returns:
        Un dictionnaire représentant la Classif1, ou None si non trouvée.
    """
    try:
        query = text("SELECT id, nom FROM Classif1 WHERE id = :id")
        result = connection.execute(query, {"id": classif1_id}).fetchone()
        if result:
            # Retourne un dictionnaire ou un modèle Pydantic
            return {"id": result[0], "nom": result[1]}
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de Classif1 par ID : {e}")
        raise # Propage l'exception

def update_classif1(connection: Session, classif1_id: int, classif1_data: Classif1Schema):
    """
    Met à jour une Classif1 existante.

    Args:
        connection: La session de base de données SQLAlchemy.
        classif1_id: L'ID de la Classif1 à mettre à jour.
        classif1_data: Les nouvelles données de la Classif1 (modèle Pydantic).

    Returns:
        Le modèle Pydantic de la Classif1 mise à jour, ou None si non trouvée.
    """
    try:
        query = text("UPDATE Classif1 SET nom = :nom WHERE id = :id")
        result = connection.execute(query, {"nom": classif1_data.nom, "id": classif1_id})
        connection.commit()
        if result.rowcount > 0:
            return classif1_data
        return None # Aucune ligne mise à jour, Classif1 non trouvée
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la mise à jour de Classif1 : {e}")
        raise # Propage l'exception

def delete_classif1(connection: Session, classif1_id: int):
    """
    Supprime une Classif1 par son ID.

    Args:
        connection: La session de base de données SQLAlchemy.
        classif1_id: L'ID de la Classif1 à supprimer.

    Returns:
        True si la suppression a réussi, False sinon.
    """
    try:
        query = text("DELETE FROM Classif1 WHERE id = :id")
        result = connection.execute(query, {"id": classif1_id})
        connection.commit()
        return result.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la suppression de Classif1 : {e}")
        raise # Propage l'exception