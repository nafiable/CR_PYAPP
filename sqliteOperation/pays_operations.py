# Fichier : sqliteOperation/pays_operations.py

from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete
from sqlalchemy.orm import sessionmaker
from sqliteOperation.connexionsqlLiter import SQLiteConnection
from schemas.Pays import Pays

# Récupérer les métadonnées pour pouvoir interagir avec les tables
# Note: Dans une application réelle, il serait préférable d'avoir une gestion centralisée
#       des métadonnées et des sessions SQLAlchemy.
#       Pour simplifier l'exemple ici, nous récupérons les métadonnées via une connexion temporaire.
try:
    temp_connection = SQLiteConnection()
    temp_engine = temp_connection.get_engine()
    metadata = MetaData()
    metadata.reflect(bind=temp_engine)
    pays_table = metadata.tables.get('Pays')
    temp_connection.close_connection()
except Exception as e:
    print(f"Erreur lors de la réflexion des métadonnées pour la table Pays: {e}")
    pays_table = None
    metadata = None


def create_pays(connection: SQLiteConnection, pays_data: dict):
    """
    Insère un nouveau pays dans la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLite.
        pays_data: Un dictionnaire contenant les données du pays.
    """
    if pays_table is None:
        print("La table 'Pays' n'a pas pu être chargée. Impossible de créer le pays.")
        return None

    engine = connection.get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Valider les données avec le modèle Pydantic si souhaité
        # pays_obj = Pays(**pays_data)
        # data_to_insert = pays_obj.model_dump()

        stmt = insert(pays_table).values(pays_data)
        result = session.execute(stmt)
        session.commit()
        # Retourne l'ID de la ligne insérée (peut varier selon le driver et la configuration)
        return result.lastrowid
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la création du pays: {e}")
        return None
    finally:
        session.close()


def get_pays_by_id(connection: SQLiteConnection, pays_id: int):
    """
    Récupère un pays par son ID depuis la base de données SQLite.

    Args:ç
 connection: L'objet de connexion SQLite.
        pays_id: L'ID du pays à récupérer.

    Returns:
        Un dictionnaire représentant le pays, ou None si non trouvé.
    """
    if pays_table is None:
        print("La table 'Pays' n'a pas pu être chargée. Impossible de récupérer le pays.")
        return None

    engine = connection.get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        stmt = select(pays_table).where(pays_table.c.id == pays_id)
        result = session.execute(stmt).fetchone()
        if result:
            # Convertir le résultat en dictionnaire
            return dict(result)
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération du pays avec ID {pays_id}: {e}")
        return None
    finally:
        session.close()


def update_pays(connection: SQLiteConnection, pays_id: int, pays_data: dict):
    """
    Met à jour un pays existant dans la base de données SQLite.

    Args:ç
 connection: L'objet de connexion SQLite.
        pays_id: L'ID du pays à mettre à jour.
        pays_data: Un dictionnaire contenant les données de mise à jour.

    Returns:
        True si la mise à jour a réussi, False sinon.
    """
    if pays_table is None:
        print("La table 'Pays' n'a pas pu être chargée. Impossible de mettre à jour le pays.")
        return False

    engine = connection.get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Valider les données de mise à jour avec le modèle Pydantic si souhaité
        # pays_obj = Pays(**pays_data) # Peut nécessiter de gérer les champs partiels
        # data_to_update = pays_obj.model_dump(exclude_unset=True) # exclure les champs non définis

        stmt = update(pays_table).where(pays_table.c.id == pays_id).values(pays_data)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount > 0  # Retourne True si au moins une ligne a été modifiée
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la mise à jour du pays avec ID {pays_id}: {e}")
        return False
    finally:
        session.close()


def delete_pays(connection: SQLiteConnection, pays_id: int):
    """
    Supprime un pays de la base de données SQLite.

    Args:ç
 connection: L'objet de connexion SQLite.
        pays_id: L'ID du pays à supprimer.

    Returns:
        True si la suppression a réussi, False sinon.
    """
    if pays_table is None:
        print("La table 'Pays' n'a pas pu être chargée. Impossible de supprimer le pays.")
        return False

    engine = connection.get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        stmt = delete(pays_table).where(pays_table.c.id == pays_id)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount > 0  # Retourne True si au moins une ligne a été supprimée
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression du pays avec ID {pays_id}: {e}")
        return False
    finally:
        session.close()