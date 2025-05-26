# sqlserverOperation/titre_operations.py

import logging
from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger(__name__)

# Import du modèle Pydantic pour la validation (si utilisé)
# from schemas.Titre import Titre
from typing import Dict, Any

def create_titre(connection: Session, titre_data: Dict[str, Any]) -> bool:
    """
    Insère un nouveau titre dans la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données SQL Server.
        titre_data: Un dictionnaire contenant les données du titre à insérer.
                    Peut être basé sur le modèle Pydantic Titre.

    Returns:
        True si l'opération réussit, False sinon.
    """
    try:
        # Exemple d'insertion basique. Adapter selon la structure exacte de la table
        query = text("""
            INSERT INTO Titre (nom, cusip, isin, ticker, emetteur, idTypeTitre1, idSousTypeTitre1, 
                               idTypeTitre2, idSecteur, idClassification1, idSousClassification1, 
                               classification2, idNotation, idPays)
            VALUES (:nom, :cusip, :isin, :ticker, :emetteur, :idTypeTitre1, :idSousTypeTitre1, 
                    :idTypeTitre2, :idSecteur, :idClassification1, :idSousClassification1, 
                    :classification2, :idNotation, :idPays)
        """)
        result = connection.execute(query, titre_data)
        # Note: SQLAlchemy Core avec text ne retourne pas l'ID inséré automatiquement.
        # Si vous avez besoin de l'ID, vous devrez utiliser l'ORM ou une clause de sortie spécifique au driver.
        # En fonction de la configuration de votre table et du driver,
        # vous pourriez avoir besoin d'une autre méthode pour récupérer l'ID inséré.
        # Par exemple, using 'OUTPUT INSERTED.ID' en SQL Server.
        # Pour l'instant, nous retournons un indicateur de succès.
        return result.rowcount == 1 # S'assurer qu'une ligne a été insérée
    except Exception as e:
        logger.error(f"Erreur lors de la création du titre : {e}", exc_info=True)
        return None

def get_titre_by_id(connection: Session, titre_id: int):
    """
    Récupère un titre par son ID depuis la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données SQL Server.
        titre_id: L'ID du titre à récupérer.

    Returns:
        Un dictionnaire représentant le titre si trouvé, None sinon.
    """
    try:
        query = text("SELECT * FROM Titre WHERE id = :titre_id")
        result = connection.execute(query, {"titre_id": titre_id}).fetchone()
        if result:
            # Convertir le résultat en dictionnaire pour une meilleure maniabilité
            return dict(result)
        return None
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du titre (ID: {titre_id}) : {e}", exc_info=True)
        return None

def update_titre(connection: Session, titre_id: int, titre_data: Dict[str, Any]) -> bool:
    """
    Met à jour un titre existant dans la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données SQL Server.
        titre_id: L'ID du titre à mettre à jour.
        titre_data: Un dictionnaire contenant les données du titre à mettre à jour.
                    Peut être basé sur le modèle Pydantic Titre (uniquement les champs à modifier).

    Returns:
        True si la mise à jour réussit, False sinon.
    """
    try:
        # Construction dynamique de la requête de mise à jour
        update_fields = ", ".join([f"{key} = :{key}" for key in titre_data.keys()])
        if not update_fields:
            return False # Rien à mettre à jour

        query = text(f"UPDATE Titre SET {update_fields} WHERE id = :titre_id")
        # Combiner les données de mise à jour avec l'ID pour l'exécution de la requête
        params = {**titre_data, "titre_id": titre_id}
        result = connection.execute(query, params)
        # Retourne True si au moins une ligne a été affectée (mise à jour réussie)
        return result.rowcount > 0
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour du titre (ID: {titre_id}) : {e}", exc_info=True)
        return None # Indiquer un échec

def delete_titre(connection: Session, titre_id: int):
    """
    Supprime un titre de la base de données SQL Server.

    Args:
        connection: Session SQLAlchemy connectée à la base de données SQL Server.
        titre_id: L'ID du titre à supprimer.

    Returns:
        True si la suppression réussit, False sinon.
    """
    try:
        query = text("DELETE FROM Titre WHERE id = :titre_id").bindparams(titre_id=titre_id)
        result = connection.execute(query)
        # Retourne True si au moins une ligne a été affectée (suppression réussie)
        return result.rowcount > 0 # Utiliser > 0 car un DELETE peut affecter 0 lignes si l'ID n'existe pas
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du titre (ID: {titre_id}) : {e}", exc_info=True)
        return False