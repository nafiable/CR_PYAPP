# sqlserverOperation/compositionfondsgestionnaire_operations.py

from sqlalchemy import text
import logging

from datetime import date
# Supposons que votre modèle CompositionFondsGestionnaire est importable
# from schemas.CompositionFondsGestionnaire import CompositionFondsGestionnaire

# Dépendance hypothetique pour la connexion, à remplacer par votre implementation
# from database.connexionsqlServer import SQLServerConnection

logger = logging.getLogger(__name__)


def create_composition(connection, composition_data: dict):
    """
    Insère une nouvelle composition de fonds par gestionnaire dans la base de données.

    Args:
        connection: L'objet de connexion à la base de données SQLAlchemy.
        composition_data (dict): Un dictionnaire contenant les données de la composition.
                                  Doit correspondre aux champs de la table CompositionFondsGestionnaire.
    """
    try:
        # Exemple d'insertion. Adaptez les noms de colonnes selon votre schema SQL réel.
        query = text("""
            INSERT INTO CompositionFondsGestionnaire (date, id_fonds, id_gestionnaire, id_Titre, id_devise, id_pays, quantite, prix, valeur_marchande, accrued, dividende)
            VALUES (:date, :id_fonds, :id_gestionnaire, :id_Titre, :id_devise, :id_pays, :quantite, :prix, :valeur_marchande, :accrued, :dividende)
        """)
        with connection.connect() as conn:
            conn.execute(query, composition_data)
            conn.commit()
        logger.info("Composition créée avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de la création de la composition : {e}")
        raise


def get_composition(connection, fonds_id: int, gestionnaire_id: int, date_composition: date):
    """
    Récupère une composition de fonds par gestionnaire spécifique par fonds, gestionnaire et date.

    Args:
        connection: L'objet de connexion à la base de données SQLAlchemy.
        fonds_id (int): L'ID du fonds.
        gestionnaire_id (int): L'ID du gestionnaire.
        date_composition (date): La date de la composition.

    Returns:
        dict ou None: Un dictionnaire représentant la composition, ou None si non trouvée.
    """
    try:
        query = text("""
            SELECT date, id_fonds, id_gestionnaire, id_Titre, id_devise, id_pays, quantite, prix, valeur_marchande, accrued, dividende
            FROM CompositionFondsGestionnaire
            WHERE id_fonds = :fonds_id AND id_gestionnaire = :gestionnaire_id AND date = :date_composition
        """)
        with connection.connect() as conn:
            result = conn.execute(query, {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date_composition": date_composition}).fetchone()
            if result:
                # Convertir le résultat en dictionnaire
                return dict(result)
            else:
                return None
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la composition : {e}")
        raise


def update_composition(connection, fonds_id: int, gestionnaire_id: int, date_composition: date, composition_data: dict):
    """
    Met à jour une composition de fonds par gestionnaire existante.

    Args:
        connection: L'objet de connexion à la base de données SQLAlchemy.
        fonds_id (int): L'ID du fonds.
        gestionnaire_id (int): L'ID du gestionnaire.
        date_composition (date): La date de la composition à mettre à jour.
        composition_data (dict): Un dictionnaire contenant les nouvelles données.
    """
    try:
        # Assurez-vous que composition_data ne contient pas les clés primaires si elles ne doivent pas être modifiées
        update_fields = ", ".join([f"{key} = :{key}" for key in composition_data.keys()])
        query = text(f"""
            UPDATE CompositionFondsGestionnaire
            SET {update_fields}
            WHERE id_fonds = :fonds_id AND id_gestionnaire = :gestionnaire_id AND date = :date_composition
        """)
        params = {**composition_data, "fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date_composition": date_composition}
        with connection.connect() as conn:
            result = conn.execute(query, params)
            conn.commit()
            if result.rowcount == 0:
                logger.warning("Aucune composition trouvée pour la mise à jour.")
            else:
                logger.info(f"{result.rowcount} composition(s) mise(s) à jour.")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de la composition : {e}")
        raise # Relève l'exception pour traitement ultérieur


def delete_composition(connection, fonds_id: int, gestionnaire_id: int, date_composition: date):
    """
    Supprime une composition de fonds par gestionnaire.

    Args:
        connection: L'objet de connexion à la base de données SQLAlchemy.
        fonds_id (int): L'ID du fonds.
        gestionnaire_id (int): L'ID du gestionnaire.
        date_composition (date): La date de la composition à supprimer.
    """
    try:
        query = text("""
            DELETE FROM CompositionFondsGestionnaire
            WHERE id_fonds = :fonds_id AND id_gestionnaire = :gestionnaire_id AND date = :date_composition
        """)
        with connection.connect() as conn:
            result = conn.execute(query, {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date_composition": date_composition})
            conn.commit()
            if result.rowcount > 0:
                logger.info(f"{result.rowcount} composition(s) supprimée(s).")
            else:
                logger.warning("Aucune composition trouvée pour la suppression.")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la composition : {e}")
        raise