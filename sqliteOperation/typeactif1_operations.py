# Fichier : sqliteOperation/typeactif1_operations.py

from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

class TypeActif1OperationsSQLite:
    """
    Gère les opérations CRUD pour la table TypeActif1 dans la base de données SQLite.
    """

    def create_typeactif1(self, connection, typeactif1_data: dict):
        """
        Insère un nouveau type d'actif 1 dans la table TypeActif1.

        Args:
            connection: Objet de connexion SQLAlchemy.
            typeactif1_data (dict): Dictionnaire contenant les données du type d'actif 1.
                                    Doit contenir au moins la clé 'type'.

        Returns:
            int: L'ID du type d'actif 1 inséré.
        """
        try:
            with connection.connect() as conn:
                result = conn.execute(
                    text("INSERT INTO TypeActif1 (type) VALUES (:type)"),
                    type=typeactif1_data.get("type")
                )
                conn.commit()
                # Pour SQLite, on peut récupérer l'ID inséré de cette manière
                inserted_id = result.lastrowid
                logger.info(f"TypeActif1 créé avec l'ID : {inserted_id}")
                return inserted_id
        except Exception as e:
            logger.error(f"Erreur lors de la création du TypeActif1 : {e}")
            raise

    def get_typeactif1_by_id(self, connection, typeactif1_id: int):
        """
        Récupère un type d'actif 1 par son ID.

        Args:
            connection: Objet de connexion SQLAlchemy.
            typeactif1_id (int): L'ID du type d'actif 1 à récupérer.

        Returns:
            dict or None: Un dictionnaire représentant le type d'actif 1 ou None s'il n'est pas trouvé.
        """
        try:
            with connection.connect() as conn:
                result = conn.execute(
                    text("SELECT id, type FROM TypeActif1 WHERE id = :id"),
                    id=typeactif1_id
                )
                row = result.fetchone()
                if row:
                    # Convertir la ligne SQLAlchemy en dictionnaire
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du TypeActif1 (ID: {typeactif1_id}) : {e}")
            raise

    def update_typeactif1(self, connection, typeactif1_id: int, typeactif1_data: dict):
        """
        Met à jour un type d'actif 1 existant.

        Args:
            connection: Objet de connexion SQLAlchemy.
            typeactif1_id (int): L'ID du type d'actif 1 à mettre à jour.
            typeactif1_data (dict): Dictionnaire contenant les données à mettre à jour.
                                    Peut contenir la clé 'type'.

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        try:
            with connection.connect() as conn:
                result = conn.execute(
                    text("UPDATE TypeActif1 SET type = :type WHERE id = :id"),
                    type=typeactif1_data.get("type"),
                    id=typeactif1_id
                )
                conn.commit()
                logger.info(f"TypeActif1 (ID: {typeactif1_id}) mis à jour.")
                return result.rowcount > 0
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du TypeActif1 (ID: {typeactif1_id}) : {e}")
            raise

    def delete_typeactif1(self, connection, typeactif1_id: int):
        """
        Supprime un type d'actif 1 par son ID.

        Args:
            connection: Objet de connexion SQLAlchemy.
            typeactif1_id (int): L'ID du type d'actif 1 à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        try:
            with connection.connect() as conn:
                result = conn.execute(
                    text("DELETE FROM TypeActif1 WHERE id = :id"),
                    id=typeactif1_id
                )
                conn.commit()
                logger.info(f"TypeActif1 (ID: {typeactif1_id}) supprimé.")
                return result.rowcount > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du TypeActif1 (ID: {typeactif1_id}) : {e}")
            raise