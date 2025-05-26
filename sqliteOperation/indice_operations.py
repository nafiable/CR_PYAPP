from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Connection
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

metadata = MetaData()

# Définition de la table Indice pour SQLAlchemy
# Assurez-vous que cette définition correspond à celle de votre script sqliteCreation.sql
indice_table = Table(
    "Indice", metadata,
    # Supposons que 'id' est la clé primaire
    # D'autres colonnes peuvent être ajoutées ici selon le schéma de la BDD
)

def create_indice(connection: Connection, indice_data: Dict[str, Any]):
    """
    Insère un nouvel indice dans la table 'Indice'.

    Args:
        connection: Objet connexion SQLAlchemy.
        indice_data: Dictionnaire contenant les données de l'indice.
                     Ex: {'nom': 'Mon Indice'} (l'ID peut être généré automatiquement par la BDD)
    """
    try:
        stmt = insert(indice_table).values(indice_data)
        result = connection.execute(stmt)
        # Si la colonne ID est auto-incrémentée, on peut récupérer l'ID inséré ainsi:
        # inserted_id = result.lastrowid
        # logger.info(f"Indice créé avec ID: {inserted_id}")
        logger.info("Indice créé.")
    except SQLAlchemyError as e:
        logger.error(f"Erreur lors de la création de l'indice : {e}")
        # La gestion des transactions dépend de comment la connexion est gérée en amont.
        # Si 'connection' est un objet Session, commit/rollback serait approprié ici.
        # Si c'est un Engine, les opérations sont auto-committées par défaut ou gérées via un 'with engine.connect() as conn:' bloc. # noqa: E501

def get_indice_by_id(connection: Connection, indice_id: int) -> Optional[Dict[str, Any]]:
    """
    Récupère un indice par son ID depuis la table 'Indice'.

    Args:
        connection: Objet connexion SQLAlchemy.
        indice_id: ID de l'indice à récupérer.

    Returns:
        Un dictionnaire représentant l'indice, ou None si non trouvé.
    """
    try:
        stmt = select(indice_table).where(indice_table.c.id == indice_id)
        result = connection.execute(stmt)
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return None
    except SQLAlchemyError as e:
        logger.error(f"Erreur lors de la récupération de l'indice (ID: {indice_id}) : {e}")
        return None

def update_indice(connection: Connection, indice_id: int, indice_data: Dict[str, Any]):
    """
    Met à jour un indice existant dans la table 'Indice'.

    Args:
        connection: Objet connexion SQLAlchemy.
        indice_id: ID de l'indice à mettre à jour.
        indice_data: Dictionnaire contenant les données à mettre à jour.
                     Ex: {'nom': 'Nouveau Nom'}
    """
    try:
        stmt = update(indice_table).where(indice_table.c.id == indice_id).values(indice_data)
        result = connection.execute(stmt)
        if result.rowcount > 0:
            logger.info(f"Indice (ID: {indice_id}) mis à jour.")
        else:
            logger.warning(f"Aucun indice trouvé avec l'ID {indice_id} pour la mise à jour.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la mise à jour de l'indice (ID: {indice_id}) : {e}")
        # La gestion des transactions dépend de comment la connexion est gérée en amont. # noqa: E501

def delete_indice(connection: Connection, indice_id: int):
    """
    Supprime un indice par son ID depuis la table 'Indice'.

    Args:
        connection: Objet connexion SQLAlchemy.
        indice_id: ID de l'indice à supprimer.
    """
    try:
        stmt = delete(indice_table).where(indice_table.c.id == indice_id)
        result = connection.execute(stmt)
        if result.rowcount > 0:
            logger.info(f"Indice (ID: {indice_id}) supprimé.")
        else:
            logger.warning(f"Aucun indice trouvé avec l'ID {indice_id} pour la suppression.")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de la suppression de l'indice (ID: {indice_id}) : {e}")