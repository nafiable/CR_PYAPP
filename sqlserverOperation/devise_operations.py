# Fichier : sqlserverOperation/devise_operations.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData, exc
from sqlalchemy.sql import select, insert, update, delete
# Base = declarative_base()

# Obtenir les métadonnées pour accéder aux tables
# Assurez-vous que les métadonnées sont chargées avec les définitions de table
# metadata = MetaData()
# Vous devrez charger les tables ici, par exemple:
# devise_table = Table('Devise', metadata, autoload_with=engine)

# Classe de connexion (à importer depuis database/connexionsqlServer.py)
# from database.connexionsqlServer import SQLServerConnection

def create_devise(connection, devise_data):
    """
    Insère une nouvelle devise dans la base de données SQL Server.

    Args:
        connection: Objet de connexion à la base de données SQL Server (fourni par SQLServerConnection).
        devise_data (dict): Dictionnaire contenant les données de la devise (ex: {'code': 'USD', 'nom': 'Dollar Américain', 'idPays': 1}).

    Returns:
        int: L'ID de la devise insérée, ou None en cas d'échec.
    """
    try:
        # Obtenir l'engine de connexion
        engine = connection.get_engine()
        # Nous allons utiliser SQLAlchemy Core pour une insertion directe
        metadata = MetaData()
 # Refléchir la base de données pour obtenir la structure de la table 'Devise'
        metadata.reflect(bind=engine, only=['Devise'])
        devise_table = metadata.tables.get('Devise')

        with engine.connect() as conn:
 with conn.begin(): # Début de la transaction
 # Construire et exécuter l'instruction d'insertion
                result = conn.execute(insert(devise_table).values(devise_data))
            # Committer la transaction
            conn.commit()
            # Retourner l'ID de la ligne insérée
            # Ici, nous allons simplifier et retourner 1 pour indiquer le succès,
            # ou vous devriez exécuter une requête pour récupérer l'ID
            return 1 # Placeholder, implémentation réelle nécessaire pour récupérer l'ID
    except Exception as e:
        print(f"Erreur lors de la création de la devise : {e}")
        return None

def get_devise_by_id(connection, devise_id):
    """
    Récupère une devise par son ID depuis la base de données SQL Server.

    Args:
        connection: Objet de connexion à la base de données SQL Server.
        devise_id (int): L'ID de la devise à récupérer.

    Returns:
        dict or None: Dictionnaire représentant la devise, ou None si non trouvée.
    """
    try:
        engine = connection.get_engine()
 # Refléchir la base de données pour obtenir la structure de la table 'Devise'
        metadata = MetaData()
        metadata.reflect(bind=engine, only=['Devise'])
        devise_table = metadata.tables.get('Devise')

        metadata.reflect(bind=engine)

            if result:
                # Convertir la ligne en dictionnaire
                return dict(result)
            else:
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération de la devise par ID : {e}")
        return None

def update_devise(connection, devise_id, devise_data):
    """
    Met à jour une devise existante dans la base de données SQL Server.

    Args:
        connection: Objet de connexion à la base de données SQL Server.
        devise_id (int): L'ID de la devise à mettre à jour.
        devise_data (dict): Dictionnaire contenant les données à mettre à jour.

    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    try:
        engine = connection.get_engine()
 # Refléchir la base de données pour obtenir la structure de la table 'Devise'
        metadata = MetaData()
        metadata.reflect(bind=engine, only=['Devise'])
        devise_table = metadata.tables.get('Devise')

        with engine.connect() as conn:
 with conn.begin(): # Début de la transaction
 # Construire et exécuter l'instruction de mise à jour
                result = conn.execute(update(devise_table).where(devise_table.c.id == devise_id).values(devise_data))
            # Committer la transaction
            conn.commit()
            # Vérifier si au moins une ligne a été affectée
            return result.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la devise : {e}")
        return False

def delete_devise(connection, devise_id):
    """
    Supprime une devise par son ID depuis la base de données SQL Server.

    Args:
        connection: Objet de connexion à la base de données SQL Server.
        devise_id (int): L'ID de la devise à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    try:
        engine = connection.get_engine()
 # Refléchir la base de données pour obtenir la structure de la table 'Devise'
        metadata = MetaData()
        metadata.reflect(bind=engine, only=['Devise'])
        devise_table = metadata.tables.get('Devise')

        with engine.connect() as conn:
 with conn.begin(): # Début de la transaction
 # Construire et exécuter l'instruction de suppression
                result = conn.execute(delete(devise_table).where(devise_table.c.id == devise_id))
            # Committer la transaction
            conn.commit()
            # Vérifier si au moins une ligne a été affectée
            return result.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la suppression de la devise : {e}")
        return False