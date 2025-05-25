# -*- coding: utf-8 -*-

from sqlalchemy import text
from datetime import date
from typing import List, Dict

class CompositionPortefeuilleGestionnaireOperations:
    """
    Classe contenant les opérations CRUD pour la table CompositionPortefeuilleGestionnaire en SQLite.
    """

    def create_composition(self, connection, composition_data: Dict):
        """
        Insère une nouvelle composition de portefeuille pour un gestionnaire.

        Args:
            connection: Objet connexion SQLAlchemy.
            composition_data (dict): Dictionnaire contenant les données de la composition.

        Returns:
            int: Le nombre de lignes insérées (normalement 1).
        """
        try:
            with connection.connect() as conn:
                # Exemple d'insertion (à adapter aux noms de colonnes réels)
                query = text("""
                    INSERT INTO CompositionPortefeuilleGestionnaire (
                        date, id_fonds, id_gestionnaire, id_Titre, id_devise,
                        id_pays, quantite, prix, valeur_marchande, accrued, dividende
                    ) VALUES (
                        :date, :id_fonds, :id_gestionnaire, :id_Titre, :id_devise,
                        :id_pays, :quantite, :prix, :valeur_marchande, :accrued, :dividende
                    )
                """)
                result = conn.execute(query, composition_data)
                conn.commit()
                return result.rowcount
        except Exception as e:
            print(f"Erreur lors de la création de la composition de portefeuille : {e}")
            raise

    def get_composition(self, connection, fonds_id: int, gestionnaire_id: int, date: date) -> List[Dict]:
        """
        Récupère la composition de portefeuille pour un fonds, un gestionnaire et une date donnés.

        Args:
            connection: Objet connexion SQLAlchemy.
            fonds_id (int): L'ID du fonds.
            gestionnaire_id (int): L'ID du gestionnaire.
            date (str): La date de la composition (format 'YYYY-MM-DD').

        Returns:
            list: Liste de dictionnaires représentant les lignes de composition.
        """
        try:
            with connection.connect() as conn:
                query = text("""
                    SELECT * FROM CompositionPortefeuilleGestionnaire
                    WHERE id_fonds = :fonds_id
                    AND id_gestionnaire = :gestionnaire_id
                    AND date = :date
                """)
                result = conn.execute(query, {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date": date})
                return [row._asdict() for row in result.fetchall()]
        except Exception as e:
            print(f"Erreur lors de la récupération de la composition de portefeuille : {e}")
            raise

    def update_composition(self, connection, fonds_id: int, gestionnaire_id: int, date: date, composition_data: Dict):
        """
        Met à jour une composition de portefeuille existante pour un fonds, un gestionnaire et une date donnés.

        Args:
            connection: Objet connexion SQLAlchemy.
            fonds_id (int): L'ID du fonds.
            gestionnaire_id (int): L'ID du gestionnaire.
            date (str): La date de la composition (format 'YYYY-MM-DD').
            composition_data (dict): Dictionnaire contenant les données de mise à jour.

        Returns:
            int: Le nombre de lignes mises à jour.
        """
        try:
            with connection.connect() as conn:
                # Adapter la clause SET en fonction des champs à mettre à jour
                set_clauses = ", ".join([f"{key} = :{key}" for key in composition_data.keys()])
                query = text(f"""
                    UPDATE CompositionPortefeuilleGestionnaire
                    SET {set_clauses}
                    WHERE id_fonds = :fonds_id
                    AND id_gestionnaire = :gestionnaire_id
                    AND date = :date
                """)
                params = {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date": date, **composition_data}
                result = conn.execute(query, params)
                conn.commit()
                return result.rowcount
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la composition de portefeuille : {e}")
            raise

    def delete_composition(self, connection, fonds_id: int, gestionnaire_id: int, date: date):
        """
        Supprime une composition de portefeuille pour un fonds, un gestionnaire et une date donnés.

        Args:
            connection: Objet connexion SQLAlchemy.
            fonds_id (int): L'ID du fonds.
            gestionnaire_id (int): L'ID du gestionnaire.
            date (str): La date de la composition (format 'YYYY-MM-DD').

        Returns:
            int: Le nombre de lignes supprimées.
        """
        try:
            with connection.connect() as conn:
                query = text("""
                    DELETE FROM CompositionPortefeuilleGestionnaire
                    WHERE id_fonds = :fonds_id
                    AND id_gestionnaire = :gestionnaire_id
                    AND date = :date
                """)
                result = conn.execute(query, {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date": date})
                conn.commit()
                return result.rowcount
        except Exception as e:
            print(f"Erreur lors de la suppression de la composition de portefeuille : {e}")
            raise