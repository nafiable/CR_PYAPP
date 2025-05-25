# sqlserverOperation/region_operations.py

from sqlalchemy import text, insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError

def create_region(connection, region_data: dict):
    """
    Insère une nouvelle région dans la base de données SQL Server.

    Args:
        connection: Objet connexion SQLAlchemy Engine/Connection.
        region_data (dict): Dictionnaire contenant les données de la région (ex: {'code': 'EU', 'nom': 'Europe'}).
                            L'ID sera généré automatiquement par la base de données si défini ainsi.
    """
    # Utilisation de l'expression insert de SQLAlchemy pour plus de robustesse
    # Utilisation d'une transaction pour garantir l'atomicité
    try:
        query = insert(text("Region")).values(**region_data)
        with connection.connect() as conn:
            with conn.begin(): # Débute la transaction
                conn.execute(query)
            # conn.commit() # Le commit est automatique à la sortie du bloc begin si aucune exception n'est levée
        # Retourne True ou l'ID inséré si nécessaire
        return True # Adapter si vous avez besoin de l'ID inséré
    except SQLAlchemyError as e:
        print(f"Erreur lors de la création de la région : {e}") # Log l'erreur
        raise # Relève l'exception pour traitement ultérieur (par ex. par le dispatcher)
    print(f"Région créée : {region_data.get('code')}") # Exemple simple, adapter selon les besoins de log

def get_region_by_id(connection, region_id: int):
    """
    Récupère une région par son ID depuis la base de données SQL Server.

    Args:
        connection: Objet connexion SQLAlchemy Engine/Connection.
        region_id (int): L'ID de la région à récupérer.

    Returns:
        dict or None: Un dictionnaire représentant la région ou None si non trouvée.
    """
    # Utilisation de l'expression select de SQLAlchemy
    try:
        query = select(text("id, code, nom")).select_from(text("Region")).where(text("id = :region_id"))
        with connection.connect() as conn:
            result = conn.execute(query, {"region_id": region_id}).fetchone()
    except SQLAlchemyError as e:
        print(f"Erreur lors de la récupération de la région ID {region_id}: {e}") # Log l'erreur
        raise # Relève l'exception

    if result: # Vérifie si un résultat a été trouvé
        return dict(result)
    return None

def update_region(connection, region_id: int, region_data: dict):
    """
    Met à jour une région existante dans la base de données SQL Server.

    Args:
        connection: Objet connexion SQLAlchemy Engine/Connection.
        region_id (int): L'ID de la région à mettre à jour.
        region_data (dict): Dictionnaire contenant les nouvelles données de la région (ex: {'nom': 'Nouvelle Europe'}).
    """
    # Utilisation de l'expression update de SQLAlchemy
    # Utilisation d'une transaction
    try:
        query = update(text("Region")).where(text("id = :region_id")).values(**region_data)
        with connection.connect() as conn:
            with conn.begin(): # Débute la transaction
                result = conn.execute(query, {"region_id": region_id})
            # conn.commit()
        # Retourne le nombre de lignes modifiées ou True si succès
        return result.rowcount > 0 # Indique si au moins une ligne a été mise à jour
    except SQLAlchemyError as e:
        print(f"Erreur lors de la mise à jour de la région ID {region_id}: {e}") # Log l'erreur
        raise # Relève l'exception
    print(f"Région ID {region_id} mise à jour.") # Exemple simple

def delete_region(connection, region_id: int):
    """
    Supprime une région par son ID depuis la base de données SQL Server.

    Args:
        connection: Objet connexion SQLAlchemy Engine/Connection.
        region_id (int): L'ID de la région à supprimer.
    """
    # Utilisation de l'expression delete de SQLAlchemy
    # Utilisation d'une transaction
    try:
        query = delete(text("Region")).where(text("id = :region_id"))
        with connection.connect() as conn:
            with conn.begin(): # Débute la transaction
                result = conn.execute(query, {"region_id": region_id})
            # conn.commit()
        # Retourne le nombre de lignes supprimées ou True si succès
        return result.rowcount > 0 # Indique si au moins une ligne a été supprimée
    except SQLAlchemyError as e:
        print(f"Erreur lors de la suppression de la région ID {region_id}: {e}") # Log l'erreur
        raise # Relève l'exception
    print(f"Région ID {region_id} supprimée.") # Exemple simple