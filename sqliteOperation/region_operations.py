# Fichier : sqliteOperation/region_operations.py

from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)
from sqlalchemy.exc import SQLAlchemyError
# from schemas.Region import Region

# Définir la table pour SQLAlchemy (à adapter si vous utilisez un ORM complet)
# Pour des opérations basiques avec SQLAlchemy Core ou texte, ceci est suffisant
# Assurez-vous que le nom de la table correspond à celui dans votre script de création
REGION_TABLE_NAME = "Region"

def create_region(connection, region_data: dict):
    """
    Insère une nouvelle région dans la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        region_data (dict): Un dictionnaire contenant les données de la région
                            (par exemple, {'code': '...', 'nom': '...'}).
                            Peut aussi accepter un modèle Pydantic de Region converti en dict.
    Returns:
        dict: Un dictionnaire indiquant le succès et les données insérées.
    """
 with connection.connect() as conn:
 with conn.begin(): # Démarre une transaction
 try:
            # Utiliser un Statement SQL textuel pour l'insertion
            # Adaptez les noms de colonnes si nécessaires
            stmt = text(f"INSERT INTO {REGION_TABLE_NAME} (code, nom) VALUES (:code, :nom)")
            result = conn.execute(stmt, region_data)
 # Si vous avez besoin de l'ID inséré, vous pouvez le récupérer ici
 # En SQLite, il est souvent accessible via lastrowid
            # inserted_id = result.lastrowid
            return {"status": "success", "message": "Région créée", "data": region_data}
        except Exception as e:
 logger.error(f"Erreur lors de la création de la région : {e}", exc_info=True)
            conn.rollback()
 return {"status": "error", "message": f"Erreur lors de la création de la région."}

def get_region_by_id(connection, region_id: int):
    """
    Récupère une région par son ID depuis la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        region_id (int): L'ID de la région à récupérer.

    Returns:
        dict or None: Un dictionnaire contenant les données de la région ou None si non trouvée.
    """
    with connection.connect() as conn:
        try:
            stmt = text(f"SELECT id, code, nom FROM {REGION_TABLE_NAME} WHERE id = :region_id;")
            result = conn.execute(stmt, {"region_id": region_id}).fetchone()
            if result:
                # Convertir le résultat en dictionnaire si nécessaire
 # Les résultats de SQLAlchemy peuvent être accédés par nom ou index
                return dict(result)
            else:
                return None
        except Exception as e:
            # En lecture, pas besoin de rollback, mais on peut logger l'erreur
 logger.error(f"Erreur lors de la récupération de la région par ID {region_id}: {e}", exc_info=True)
            return None

def update_region(connection, region_id: int, region_data: dict):
    """
    Met à jour une région existante dans la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        region_id (int): L'ID de la région à mettre à jour.
        region_data (dict): Un dictionnaire contenant les données à mettre à jour
                            (par exemple, {'code': 'NOUVEAU_CODE', 'nom': 'Nouveau Nom'}).

    Returns:
        dict: Un dictionnaire indiquant le succès ou l'échec de la mise à jour.
    """
 with connection.connect() as conn:
 with conn.begin(): # Démarre une transaction
 try:
            # Construire la partie SET de la requête dynamiquement si `region_data` est variable
            set_clauses = ", ".join([f"{key} = :{key}" for key in region_data])
            if not set_clauses:
                return {"status": "error", "message": "Aucune donnée à mettre à jour"}

            stmt = text(f"UPDATE {REGION_TABLE_NAME} SET {set_clauses} WHERE id = :region_id;")
            # Fusionner les données de mise à jour avec l'ID pour l'exécution
            update_params = {**region_data, "region_id": region_id}
            result = conn.execute(stmt, update_params)
            if result.rowcount > 0:
 logger.info(f"Région avec ID {region_id} mise à jour.")
 return {"status": "success", "message": f"Région avec ID {region_id} mise à jour."}
            else:
 logger.warning(f"Région avec ID {region_id} non trouvée ou aucune modification.")
 return {"status": "warning", "message": f"Région avec ID {region_id} non trouvée ou aucune modification."}
        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": f"Erreur lors de la mise à jour de la région : {e}"}

def delete_region(connection, region_id: int):
    """
    Supprime une région par son ID depuis la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        region_id (int): L'ID de la région à supprimer.

    Returns:
        dict: Un dictionnaire indiquant le succès ou l'échec de la suppression.
    """
 with connection.connect() as conn:
 with conn.begin(): # Démarre une transaction
 try:
            stmt = text(f"DELETE FROM {REGION_TABLE_NAME} WHERE id = :region_id;")
            result = conn.execute(stmt, {"region_id": region_id})
            if result.rowcount > 0:
 logger.info(f"Région avec ID {region_id} supprimée.")
 return {"status": "success", "message": f"Région avec ID {region_id} supprimée."}
            else:
 logger.warning(f"Région avec ID {region_id} non trouvée.")
 return {"status": "warning", "message": f"Région avec ID {region_id} non trouvée."}
        except SQLAlchemyError as e:
            conn.rollback()
            return {"status": "error", "message": f"Erreur lors de la suppression de la région : {e}"}

# Exemple d'utilisation (pourrait être dans un script de test)
# if __name__ == "__main__":
#     # Assurez-vous d'avoir initialisé la connexion
#     # from database.connexionsqlLiter import SQLiteConnection
#     # db_connection = SQLiteConnection().get_engine()
#
#     # Exemple de création
#     # new_region_data = {"code": "EU", "nom": "Europe"}
#     # result_create = create_region(db_connection, new_region_data)
#     # print(result_create)
#
#     # Exemple de lecture
#     # region = get_region_by_id(db_connection, 1) # Supposons que l'ID 1 existe
#     # print(region)
#
#     # Exemple de mise à jour
#     # update_data = {"nom": "Europe Continentale"}
#     # result_update = update_region(db_connection, 1, update_data)
#     # print(result_update)
#
#     # Exemple de suppression
#     # result_delete = delete_region(db_connection, 1)
#     # print(result_delete)