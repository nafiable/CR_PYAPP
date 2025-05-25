# sqliteOperation/secteur_operations.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import text

# Assurez-vous d'avoir un modèle Sector correspondant si vous utilisez l'ORM
# from schemas.Secteur import Secteur # Exemple si vous utilisez l'ORM

def create_secteur(connection: Session, secteur_data: dict):
    """
    Crée un nouveau secteur dans la base de données SQLite.

    Args:
        connection: L'objet connexion SQLAlchemy (Session).
        secteur_data: Un dictionnaire contenant les données du secteur (ex: {'codeGics': '...', 'codeBics': '...', 'nom': '...'}).

    Returns:
        L'ID du secteur créé.
    """
 # Utiliser un bloc 'with' pour la transaction
 with connection.begin():
    try:
        # Exemple d'utilisation d'une requête brute
        query = text("INSERT INTO Secteur (codeGics, codeBics, nom) VALUES (:codeGics, :codeBics, :nom)")
        result = connection.execute(query, secteur_data)
        # Pour SQLite, on peut récupérer l'ID inséré comme ceci
 # SQLAlchemy utilise .lastrowid pour les moteurs qui le supportent, y compris SQLite
 return result.lastrowid
 # Gérer les erreurs spécifiques si possible
 except IntegrityError as e:
 print(f"Erreur d'intégrité lors de la création du secteur : {e}")
 # Lever l'exception pour signaler l'échec au niveau supérieur
 raise
 except SQLAlchemyError as e:
        connection.rollback()
        print(f"Erreur lors de la création du secteur : {e}")
        return None

def get_secteur_by_id(connection: Session, secteur_id: int):
    """
    Récupère un secteur par son ID depuis la base de données SQLite.

    Args:
        connection: L'objet connexion SQLAlchemy (Session).
        secteur_id: L'ID du secteur à récupérer.

    Returns:
        Un dictionnaire représentant le secteur ou None si non trouvé.
    """
    try:
        query = text("SELECT id, codeGics, codeBics, nom FROM Secteur WHERE id = :id")
        result = connection.execute(query, {"id": secteur_id}).fetchone()
        if result:
            # Convertir le résultat en dictionnaire
            return dict(result)
        return None
 except SQLAlchemyError as e:
 # Pas besoin de rollback pour une lecture simple
 print(f"Erreur lors de la récupération du secteur (ID: {secteur_id}): {e}")
 # Lever l'exception pour signaler l'échec au niveau supérieur
        raise
        return None

def update_secteur(connection: Session, secteur_id: int, secteur_data: dict):
    """
    Met à jour un secteur existant dans la base de données SQLite.

    Args:
        connection: L'objet connexion SQLAlchemy (Session).
        secteur_id: L'ID du secteur à mettre à jour.
        secteur_data: Un dictionnaire contenant les données à mettre à jour.

    Returns:
        True si la mise à jour a réussi, False sinon.
    """
 # Utiliser un bloc 'with' pour la transaction
 with connection.begin():
    try:
        # Construire dynamiquement la partie SET de la requête
        set_clauses = ", ".join([f"{key} = :{key}" for key in secteur_data.keys()])
        query = text(f"UPDATE Secteur SET {set_clauses} WHERE id = :id")
        params = {"id": secteur_id, **secteur_data}
        result = connection.execute(query, params)
 # Gérer les erreurs spécifiques si possible
 except IntegrityError as e:
 print(f"Erreur d'intégrité lors de la mise à jour du secteur (ID: {secteur_id}): {e}")
        raise
        return result.rowcount > 0
    except Exception as e:
 connection.rollback()
        print(f"Erreur lors de la mise à jour du secteur (ID: {secteur_id}): {e}")
        return False

def delete_secteur(connection: Session, secteur_id: int):
    """
    Supprime un secteur de la base de données SQLite.

    Args:
        connection: L'objet connexion SQLAlchemy (Session).
        secteur_id: L'ID du secteur à supprimer.

    Returns:
        True si la suppression a réussi, False sinon.
    """
 # Utiliser un bloc 'with' pour la transaction
 with connection.begin():
    try:
        query = text("DELETE FROM Secteur WHERE id = :id")
        result = connection.execute(query, {"id": secteur_id})
        return result.rowcount > 0
 # Gérer les erreurs spécifiques si possible
 except SQLAlchemyError as e:
 connection.rollback()
 print(f"Erreur lors de la suppression du secteur (ID: {secteur_id}): {e}")
        raise