# Fichier : sqlserverOperation/sousclassif1_operations.py

import logging
from sqlalchemy import Column, Integer, String, MetaData, Table, insert, select, update, delete
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Metadonnées pour les tables
metadata = MetaData()

# Définition de la table SousClassif1 (à adapter si votre schéma SQL est différent)
# Assurez-vous que cette définition correspond exactement à celle de votre base de données
sousclassif1_table = Table(
    'SousClassif1', metadata,
    Column('id', Integer, primary_key=True),
    Column('idClassif1', Integer),  # Supposons que c'est un lien vers Classif1
    Column('nom', String(255)), # Utiliser une longueur pour VARCHAR
    # Assurez-vous que les autres colonnes correspondent à votre schéma
    # Exemple: Column('autre_colonne', TypeSQL...),
)

def create_sousclassif1(connection, sousclassif1_data):
    """
    Crée une nouvelle entrée dans la table SousClassif1.

    Args:
        connection: Objet de connexion SQLAlchemy (engine).
        sousclassif1_data (dict or schemas.SousClassif1): Données de la sous-classification à créer.
    """
    # Assurez-vous que sousclassif1_data est un dictionnaire
    if not isinstance(sousclassif1_data, dict):
        sousclassif1_data = sousclassif1_data.model_dump() # ou .dict() pour Pydantic v1

    with connection.connect() as conn:
        # Démarrer une transaction
        with conn.begin():
            insert_statement = sousclassif1_table.insert().values(sousclassif1_data)
            result = conn.execute(insert_statement)
            logger.info(f"SousClassif1 créée avec l'ID : {result.lastrowid}")

def get_sousclassif1_by_id(connection, sousclassif1_id):
    """
    Récupère une entrée (ligne) de la table SousClassif1 par son ID.

    Args:
        connection: Objet de connexion SQLAlchemy (engine).
        sousclassif1_id (int): L'ID de la sous-classification à récupérer.

    Returns:
        dict: Les données de la sous-classification ou None si non trouvée.
    """
    with connection.connect() as conn:
        select_statement = sousclassif1_table.select().where(sousclassif1_table.c.id == sousclassif1_id)
        result = conn.execute(select_statement).first() # first() est plus approprié pour un single row
        if result:
            # Convertir le résultat en dictionnaire
            return dict(result)
        return None

def update_sousclassif1(connection, sousclassif1_id, sousclassif1_data):
    """
    Met à jour une entrée existante dans la table SousClassif1.

    Args:
        connection: Objet de connexion SQLAlchemy (engine).
        sousclassif1_id (int): L'ID de la sous-classification à mettre à jour.
        sousclassif1_data (dict or schemas.SousClassif1): Nouvelles données de la sous-classification.

    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    # Assurez-vous que sousclassif1_data est un dictionnaire
    if not isinstance(sousclassif1_data, dict):
        sousclassif1_data = sousclassif1_data.model_dump() # ou .dict() pour Pydantic v1

    with connection.connect() as conn:
        with conn.begin():
            update_statement = sousclassif1_table.update().where(sousclassif1_table.c.id == sousclassif1_id).values(**sousclassif1_data) # Utiliser ** pour déballer le dict
            result = conn.execute(update_statement)
            # rowcount indique le nombre de lignes affectées
            return result.rowcount > 0

def delete_sousclassif1(connection, sousclassif1_id):
    """
    Supprime une entrée de la table SousClassif1 par son ID.

    Args:
        connection: Objet de connexion SQLAlchemy (engine).
        sousclassif1_id (int): L'ID de la sous-classification à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    with connection.connect() as conn:
        with conn.begin():
            delete_statement = sousclassif1_table.delete().where(sousclassif1_table.c.id == sousclassif1_id)
            result = conn.execute(delete_statement)
            # rowcount indique le nombre de lignes affectées
            return result.rowcount > 0

# Note : Vous devrez adapter les noms de colonnes et les types
# dans la définition de `sousclassif1_table` pour correspondre
# exactement à votre schéma de base de données SQL Server.