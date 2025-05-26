# sqlserverOperation/secteur_operations.py

from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from sqlalchemy.exc import SQLAlchemyError
# Assurez-vous d'avoir un modèle SQLAlchemy ou utilisez des requêtes brutes.
# Pour cet exemple, nous allons utiliser des requêtes brutes via la connexion brute ou l'engine.

# Supposons que 'connection' est un objet SQLAlchemy Engine ou une Session
# Assurez-vous que la table 'Secteur' existe dans votre base de données SQL Server.

logger = logging.getLogger(__name__)
def create_secteur(connection, secteur_data: dict):
    """
    Insère un nouveau secteur dans la base de données SQL Server.

    Args:
        connection: L'objet de connexion SQLAlchemy (Engine ou Session).
        secteur_data: Un dictionnaire contenant les données du secteur (par exemple, {'codeGics': '...', 'codeBics': '...', 'nom': '...'}).
                      L'ID sera généré par la base de données.

    Returns:
        int: L'ID du secteur créé, ou None en cas d'échec.
    """
    try:
        # Exemple avec une session
        if isinstance(connection, Session):
            with connection.begin():
                result = connection.execute(
 text("INSERT INTO Secteur (codeGics, codeBics, nom) VALUES (:codeGics, :codeBics, :nom); SELECT SCOPE_IDENTITY();"),
                    secteur_data
                )
                # Récupérer l'ID inséré (spécifique à SQL Server)
                secteur_id = result.scalar_one()
                return secteur_id
        else:
 # Exemple avec un engine
            with connection.connect() as conn:
                 with conn.begin():
                    result = conn.execute(
 text("INSERT INTO Secteur (codeGics, codeBics, nom) VALUES (:codeGics, :codeBics, :nom); SELECT SCOPE_IDENTITY();"),
                        secteur_data
                    )
                    secteur_id = result.scalar_one()
                    return secteur_id
    except SQLAlchemyError as e:
        print(f"Erreur lors de la création du secteur : {e}")
        logger.error(f"Erreur lors de la création du secteur : {e}")

def get_secteur_by_id(connection, secteur_id: int):
    """
    Récupère un secteur par son ID depuis la base de données SQL Server.

    Args:
        connection: L'objet de connexion SQLAlchemy (Engine ou Session).
        secteur_id: L'ID du secteur à récupérer.

    Returns:
        dict: Un dictionnaire représentant le secteur, ou None si non trouvé.
    """
    try:
        if isinstance(connection, Session):
            result = connection.execute(
                text("SELECT id, codeGics, codeBics, nom FROM Secteur WHERE id = :secteur_id"),
                {"secteur_id": secteur_id}
            ).fetchone()
        else:
             with connection.connect() as conn:
 result = conn.execute(
                    text("SELECT id, codeGics, codeBics, nom FROM Secteur WHERE id = :secteur_id"),
                    {"secteur_id": secteur_id}
                ).fetchone()
        if result:
            # Convertir le résultat en dictionnaire
            return dict(result._mapping)
        return None
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du secteur (ID: {secteur_id}): {e}")
        return None

def update_secteur(connection, secteur_id: int, secteur_data: dict):
    """
    Met à jour un secteur existant dans la base de données SQL Server.

    Args:
        connection: L'objet de connexion SQLAlchemy (Engine ou Session).
        secteur_id: L'ID du secteur à mettre à jour.
        secteur_data: Un dictionnaire contenant les données à mettre à jour (par exemple, {'nom': 'Nouveau Nom'}).

    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    try:
        if isinstance(connection, Session):
             with connection.begin():
 result = connection.execute(
                    text("UPDATE Secteur SET codeGics = :codeGics, codeBics = :codeBics, nom = :nom WHERE id = :id"),
                    {"id": secteur_id, **secteur_data}
                )
                return result.rowcount > 0
        else:
            with connection.connect() as conn:
 with conn.begin():
                    result = conn.execute(
                        text("UPDATE Secteur SET codeGics = :codeGics, codeBics = :codeBics, nom = :nom WHERE id = :id"),
                        {"id": secteur_id, **secteur_data}
                    )
                    return result.rowcount > 0
    except SQLAlchemyError as e:
        print(f"Erreur lors de la mise à jour du secteur : {e}")
        logger.error(f"Erreur lors de la mise à jour du secteur : {e}")

def delete_secteur(connection, secteur_id: int):
    """
    Supprime un secteur par son ID de la base de données SQL Server.

    Args:
        connection: L'objet de connexion SQLAlchemy (Engine ou Session).
        secteur_id: L'ID du secteur à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    try:
        if isinstance(connection, Session):
             with connection.begin():
 result = connection.execute(
                    text("DELETE FROM Secteur WHERE id = :secteur_id"),
                    {"secteur_id": secteur_id}
                )
                return result.rowcount > 0
        else:
            with connection.connect() as conn:
 with conn.begin():
                    result = conn.execute(
                        text("DELETE FROM Secteur WHERE id = :secteur_id"),
                        {"secteur_id": secteur_id}
                    )
                    return result.rowcount > 0
    except SQLAlchemyError as e:
        print(f"Erreur lors de la suppression du secteur : {e}")
        return False