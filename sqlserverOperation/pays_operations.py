# sqlserverOperation/pays_operations.py

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

# Les fonctions CRUD pour l'entité Pays utilisant SQLAlchemy

def create_pays(connection: Connection, pays_data: dict):
    """
    Insère un nouveau pays dans la table Pays.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        pays_data: Un dictionnaire contenant les données du pays

        # Exemple:
                   (par exemple, {'code': 'FR', 'nom': 'France', 'idRegion': 1, ...}).
    Returns:
        True si l'insertion a réussi, False sinon.
    """
    try:
        # Début de la transaction
        with connection.begin():
            query = text(
                "INSERT INTO Pays (code, nom, idRegion, continent, idDevise) "
                "VALUES (:code, :nom, :idRegion, :continent, :idDevise)"
            )
            connection.execute(query, pays_data)
            # La transaction est automatiquement commitée si tout se passe bien
        return True
    except SQLAlchemyError as e:
        # En cas d'erreur, la transaction est automatiquement rollbackée
        print(f"Erreur lors de la création du pays: {e}") # ou utiliser un système de logging
        return False

def get_pays_by_id(connection: Connection, pays_id: int):
    """
    Récupère un pays par son ID.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        pays_id: L'ID du pays à récupérer.
    Returns:
        Les données du pays sous forme de dictionnaire ou None si non trouvé.
    """
    try:
        query = text("SELECT id, code, nom, idRegion, continent, idDevise FROM Pays WHERE id = :pays_id")
        result = connection.execute(query, {'pays_id': pays_id}).fetchone()
        if result:
            return dict(result)
        return None
    except SQLAlchemyError as e:
        print(f"Erreur lors de la récupération du pays par ID: {e}") # ou utiliser un système de logging
        return None


def update_pays(connection: Connection, pays_id: int, pays_data: dict):
    """
    Met à jour un pays existant par son ID.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        pays_id: L'ID du pays à mettre à jour.
        pays_data: Un dictionnaire contenant les données à mettre à jour.
    Returns:
        True si la mise à jour a réussi, False sinon.
    """
    try:
        # Début de la transaction
        with connection.begin():
            # Construire dynamiquement la partie SET de la requête
            set_clauses = [f"{key} = :{key}" for key in pays_data.keys()]
            query = text(
                f"UPDATE Pays SET {', '.join(set_clauses)} WHERE id = :pays_id"
            )
            # Ajouter l'id dans les paramètres
            params = {**pays_data, 'pays_id': pays_id}
            connection.execute(query, params)
            # La transaction est automatiquement commitée
        return True
    except SQLAlchemyError as e:
        print(f"Erreur lors de la mise à jour du pays: {e}") # ou utiliser un système de logging
        return False

def delete_pays(connection: Connection, pays_id: int):
    """
    Supprime un pays par son ID.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        pays_id: L'ID du pays à supprimer.
    Returns:
        Le résultat de l'exécution de la requête.
        True si la suppression a réussi, False sinon.
    """
    try:
        # Début de la transaction
        with connection.begin():
            query = text("DELETE FROM Pays WHERE id = :pays_id")
            connection.execute(query, {'pays_id': pays_id})
            # La transaction est automatiquement commitée
        return True
    except SQLAlchemyError as e:
        print(f"Erreur lors de la suppression du pays: {e}") # ou utiliser un système de logging
        return False