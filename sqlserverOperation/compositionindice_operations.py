# sqlserverOperation/compositionindice_operations.py

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, List

# Import du modèle si l'ORM est utilisé pour certaines opérations ou validations
# Dépendance vers les schémas si nécessaire, par exemple :
# from schemas.CompositionIndice import CompositionIndice

def create_composition(connection: Session, composition_data: Dict[str, Any]):
    """
    Insère une nouvelle composition d'indice dans la base de données SQL Server.

    Args:
        connection: La session de connexion SQLAlchemy.
        composition_data: Un dictionnaire contenant les données de la composition.
                          Ex: {'date': 'YYYY-MM-DD', 'id_indice': 1, 'id_titre': 10, ...}
    """
    try:
        # Exemple d'insertion. Adapter selon les colonnes réelles de la table CompositionIndice
        query = text("""
            INSERT INTO CompositionIndice (date, id_indice, id_titre, quantite, prix, valeur_marchande, dividende)
            VALUES (:date, :id_indice, :id_titre, :quantite, :prix, :valeur_marchande, :dividende)
        """)
        connection.execute(query, composition_data)
        connection.commit()
        print("Composition d'indice insérée avec succès.")
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de l'insertion de la composition d'indice : {e}")
        raise

def get_composition(connection: Session, indice_id: int, date: str):
    """
    Récupère une composition d'indice spécifique par ID indice et date.

    Args:
        connection: La session de connexion SQLAlchemy.
        indice_id: L'ID de l'indice.
        date: La date de la composition (format 'YYYY-MM-DD').

    Returns:
        Une liste de dictionnaires représentant les lignes trouvées, ou une liste vide.
    """
 try:
        query = text("""
            SELECT date, id_indice, id_titre, quantite, prix, valeur_marchande, dividende
            FROM CompositionIndice
            WHERE id_indice = :indice_id AND date = :date
        """)
        result = connection.execute(query, {'indice_id': indice_id, 'date': date}).fetchall()
        # Convertir les lignes SQLAlchemy en liste de dictionnaires
        return [dict(row._mapping) for row in result]
 except Exception as e:
        print(f"Erreur lors de la récupération de la composition d'indice : {e}")
        return []

def update_composition(connection: Session, indice_id: int, date: str, composition_data: Dict[str, Any]):
    """
    Met à jour une composition d'indice existante par ID indice et date.

    Args:
        connection: La session de connexion SQLAlchemy.
        indice_id: L'ID de l'indice.
        date: La date de la composition (format 'YYYY-MM-DD').
        composition_data: Un dictionnaire contenant les données à mettre à jour.
                          Ex: {'quantite': 100.5, 'prix': 25.0}
    """
    try:
        # Construit dynamiquement la partie SET de la requête
        set_clauses = ", ".join([f"{key} = :{key}" for key in composition_data.keys()])
        query = text(f"""
            UPDATE CompositionIndice
            SET {set_clauses}
            WHERE id_indice = :indice_id AND date = :date
        """)
        params = {'indice_id': indice_id, 'date': date, **composition_data}
        result = connection.execute(query, params)
        connection.commit()
        if result.rowcount > 0:
            print("Composition d'indice mise à jour avec succès.")
        else:
            print("Aucune composition d'indice trouvée pour la mise à jour.")
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la mise à jour de la composition d'indice : {e}")
        raise

def delete_composition(connection: Session, indice_id: int, date: str):
    """
    Supprime une composition d'indice par ID indice et date.

    Args:
        connection: La session de connexion SQLAlchemy.
        indice_id: L'ID de l'indice.
        date: La date de la composition (format 'YYYY-MM-DD').
    """
    try:
        query = text("""
            DELETE FROM CompositionIndice
            WHERE id_indice = :indice_id AND date = :date
        """)
        result = connection.execute(query, {'indice_id': indice_id, 'date': date})
        connection.commit()
        if result.rowcount > 0:
            print("Composition d'indice supprimée avec succès.")
        else:
            print("Aucune composition d'indice trouvée pour la suppression.")
    except Exception as e:
        connection.rollback()
        print(f"Erreur lors de la suppression de la composition d'indice : {e}")
        raise