# sqliteOperation/compositionfondsgestionnaire_operations.py

import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.CompositionFondsGestionnaire import CompositionFondsGestionnaire

logger = logging.getLogger(__name__)

# Remarque : Pour un véritable ORM, on définirait ici les classes modèles SQLAlchemy.
# Pour l'instant, nous utiliserons des requêtes brutes ou des outils simples.

def create_composition(connection, composition_data: CompositionFondsGestionnaire):
    """
    Insère une nouvelle composition de fonds par gestionnaire dans la base de données SQLite.

    Args:
        connection: L'engine SQLAlchemy.
        composition_data (CompositionFondsGestionnaire): Données de la composition à insérer.

    Returns:
        bool: True si l'insertion réussit, False sinon.
    """
    try:
 with Session(connection) as session:
 # Utilisation de l'ORM SQLAlchemy pour une insertion plus propre et sécurisée
 # Nécessite une définition ORM de la table CompositionFondsGestionnaire
 # Pour l'exemple, nous allons continuer avec la méthode plus directe en attendant
 # la définition ORM ou Core pour les opérations.
 # Si on utilise SQLAlchemy Core:
 from sqlalchemy import Table, MetaData

 metadata = MetaData()
 composition_table = Table(
 'CompositionFondsGestionnaire',
 metadata,
 autoload_with=connection # Charge la structure de la table existante
 )

 stmt = composition_table.insert().values(
 date=composition_data.date,
 id_fonds=composition_data.id_fonds,
 id_gestionnaire=composition_data.id_gestionnaire,
 id_Titre=composition_data.id_Titre,
 id_devise=composition_data.id_devise,
 id_pays=composition_data.id_pays,
 quantite=composition_data.quantite,
 prix=composition_data.prix,
 valeur_marchande=composition_data.valeur_marchande,
 accrued=composition_data.accrued,
 dividende=composition_data.dividende,
            )
 session.execute(stmt)
 session.commit()
        return True
    except SQLAlchemyError as ex:
        logger.error(f"Erreur SQLAlchemy lors de la création de la composition: {ex}")
        # Gérer l'erreur (logging, etc.)
        return False

def get_composition(connection, fonds_id: int, gestionnaire_id: int, date: str):
    """
    Récupère la composition d'un fonds pour un gestionnaire à une date donnée depuis SQLite.

    Args:
        connection: L'engine SQLAlchemy.
        fonds_id (int): L'ID du fonds.
        gestionnaire_id (int): L'ID du gestionnaire.
        date (str): La date de la composition (format 'YYYY-MM-DD').

    Returns:
        list[dict] ou None: Liste de dictionnaires représentant les lignes de composition, ou None en cas d'erreur.
    """
    try:
        with connection.connect() as conn:
 # Utilisation de SQLAlchemy Core pour la sélection
 from sqlalchemy import Table, MetaData, select, and_

 metadata = MetaData()
 composition_table = Table(
 'CompositionFondsGestionnaire',
 metadata,
 autoload_with=connection
 )

 stmt = select(composition_table).where(and_(composition_table.c.id_fonds == fonds_id, composition_table.c.id_gestionnaire == gestionnaire_id, composition_table.c.date == date))
 result = conn.execute(stmt).fetchall()
            # Convertir les résultats en liste de dictionnaires
 # Utilisez result._metadata.keys si result est un ResultProxy
 compositions = [dict(row._mapping) for row in result] if result else []
            return compositions
    except SQLAlchemyError as e:
        logger.error(f"Erreur SQLAlchemy lors de la récupération de la composition: {e}")
        # Gérer l'erreur (logging, etc.)
        return None

def update_composition(connection, fonds_id: int, gestionnaire_id: int, date: str, composition_data: dict):
    """
    Met à jour une composition de fonds par gestionnaire existante dans SQLite.

    Args:
        connection: L'engine SQLAlchemy.
        fonds_id (int): L'ID du fonds.
        gestionnaire_id (int): L'ID du gestionnaire.
        date (str): La date de la composition (format 'YYYY-MM-DD').
        composition_data (dict): Dictionnaire contenant les champs à mettre à jour et leurs nouvelles valeurs.

    Returns:
        bool: True si la mise à jour réussit, False sinon.
    """
    try:
        with connection.connect() as conn:
 # Utilisation de SQLAlchemy Core pour la mise à jour
 from sqlalchemy import Table, MetaData, update, and_

 metadata = MetaData()
 composition_table = Table(
 'CompositionFondsGestionnaire',
 metadata,
 autoload_with=connection
 )

 stmt = update(composition_table).where(and_(composition_table.c.id_fonds == fonds_id, composition_table.c.id_gestionnaire == gestionnaire_id, composition_table.c.date == date)).values(composition_data)
 with conn.begin(): # Utilisation d'une transaction pour la mise à jour
                result = conn.execute(stmt)
 # conn.commit() # Commit géré par le `with conn.begin()`
            return result.rowcount > 0  # Retourne True si au moins une ligne a été affectée
    except SQLAlchemyError as ex:
        logger.error(f"Erreur SQLAlchemy lors de la mise à jour de la composition: {ex}")
        # Gérer l'erreur (logging, etc.)
        return False

def delete_composition(connection, fonds_id: int, gestionnaire_id: int, date: str):
    """
    Supprime une composition de fonds par gestionnaire de la base de données SQLite.

    Args:
        connection: L'engine SQLAlchemy.
        fonds_id (int): L'ID du fonds.
        gestionnaire_id (int): L'ID du gestionnaire.
        date (str): La date de la composition (format 'YYYY-MM-DD').

    Returns:
 bool: True si la suppression réussit, False sinon.
    """
    try:
        with connection.connect() as conn:
 # Utilisation de SQLAlchemy Core pour la suppression
 from sqlalchemy import Table, MetaData, delete, and_

 metadata = MetaData()
 composition_table = Table(
 'CompositionFondsGestionnaire',
 metadata,
 autoload_with=connection
 )

 stmt = delete(composition_table).where(and_(composition_table.c.id_fonds == fonds_id, composition_table.c.id_gestionnaire == gestionnaire_id, composition_table.c.date == date))
 result = conn.execute(stmt)
            return result.rowcount > 0  # Retourne True si au moins une ligne a été affectée
    except SQLAlchemyError as e:
        logger.error(f"Erreur SQLAlchemy lors de la suppression de la composition: {e}")
        # Gérer l'erreur (logging, etc.)
        return False