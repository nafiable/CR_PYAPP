# Fichier : sqliteOperation/titre_operations.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, text, update, delete, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from schemas.Titre import Titre  # Assurez-vous que le modèle Titre est correctement importé

# Remarque : Les mappings SQLAlchemy vers les tables devraient idéalement être définis
# de manière centrale, par exemple dans le dossier schemas ou un sous-module database.
# Pour cet exemple, nous allons simuler les opérations sans mapper explicitement
# les classes aux tables ici. L'objet 'connection' passé aux fonctions
# est supposé être un objet engine ou session SQLAlchemy.

def create_titre(connection, titre_data: Titre):
    """
    Insère un nouveau titre dans la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy (engine ou session).
        titre_data (Titre): Les données du titre à insérer.

    Returns:
        bool: True si l'insertion a réussi, False sinon.
    """
    try:
        # Simulation d'une insertion (remplacer par la vraie logique SQLAlchemy)
        # Utilisation de SQLAlchemy Core pour l'insertion
        query = text("""
            INSERT INTO Titre (id, nom, cusip, isin, ticker, emetteur, idTypeTitre1, idSousTypeTitre1, idTypeTitre2, idSecteur, idClassification1, idSousClassification1, classification2, idNotation, idPays)
            VALUES (:id, :nom, :cusip, :isin, :ticker, :emetteur, :idTypeTitre1, :idSousTypeTitre1, :idTypeTitre2, :idSecteur, :idClassification1, :idSousClassification1, :classification2, :idNotation, :idPays)
        """)
        connection.execute(query, titre_data.model_dump())
        # En cas de succès simulé
        return True
    except SQLAlchemyError as e:
        print(f"Erreur lors de la création du titre : {e}")
        # Si vous utilisiez des sessions, il faudrait rollback en cas d'erreur
        # session.rollback()
        return False

def get_titre_by_id(connection, titre_id: int):
    """
    Récupère un titre par son ID depuis la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy (engine ou session).
        titre_id (int): L'ID du titre à récupérer.

    Returns:
        dict ou None: Les données du titre sous forme de dictionnaire, ou None si non trouvé.
    """
    try:
        # Simulation d'une lecture (remplacer par la vraie logique SQLAlchemy)
        # Utilisation de SQLAlchemy Core pour la lecture
        query = text("SELECT id, nom, cusip, isin, ticker, emetteur, idTypeTitre1, idSousTypeTitre1, idTypeTitre2, idSecteur, idClassification1, idSousClassification1, classification2, idNotation, idPays FROM Titre WHERE id = :titre_id")
        result = connection.execute(query, {"titre_id": titre_id}).fetchone()
        if result:
            return {"id": result[0], "nom": result[1], "cusip": result[2], "isin": result[3], "ticker": result[4], "emetteur": result[5],
                    "idTypeTitre1": 1, "idSousTypeTitre1": 1, "idTypeTitre2": 1, "idSecteur": 1, "idClassification1": 1,
                    "idSousClassification1": 1, "classification2": "Sim Class 2", "idNotation": 1, "idPays": 1}
        else:
            return None
    except SQLAlchemyError as e:
        print(f"Erreur lors de la récupération du titre : {e}")
        return None

def update_titre(connection, titre_id: int, titre_data: Titre):
    """
    Met à jour un titre existant dans la base de données SQLite.

    Args:
        connection: L'objet de connexion SQLAlchemy (engine ou session).
        titre_id (int): L'ID du titre à mettre à jour.
        titre_data (Titre): Les nouvelles données du titre.

    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    try:
        # Simulation d'une mise à jour (remplacer par la vraie logique SQLAlchemy)
        # Utilisation de SQLAlchemy Core pour la mise à jour
        query = text("""
            UPDATE Titre
            SET nom = :nom, cusip = :cusip, isin = :isin, ticker = :ticker, emetteur = :emetteur,
                idTypeTitre1 = :idTypeTitre1, idSousTypeTitre1 = :idSousTypeTitre1, idTypeTitre2 = :idTypeTitre2,
                idSecteur = :idSecteur, idClassification1 = :idClassification1, idSousClassification1 = :idSousClassification1,
                classification2 = :classification2, idNotation = :idNotation, idPays = :idPays WHERE id = :id""")
        connection.execute(query, {**titre_data.model_dump(), "id": titre_id})
        return True
    except SQLAlchemyError as e:
        print(f"Erreur lors de la mise à jour du titre : {e}")
        # Si vous utilisiez des sessions, il faudrait rollback en cas d'erreur
        # session.rollback()
        return False

def delete_titre(connection, titre_id: int):
    """
    Supprime un titre de la base de données SQLite par son ID.

    Args:
        connection: L'objet de connexion SQLAlchemy (engine ou session).
        titre_id (int): L'ID du titre à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    try:
        # Simulation d'une suppression (remplacer par la vraie logique SQLAlchemy)
        # Utilisation de SQLAlchemy Core pour la suppression
        query = text("DELETE FROM Titre WHERE id = :titre_id")
        connection.execute(query, {"titre_id": titre_id})
        return True
    except SQLAlchemyError as e:
        print(f"Erreur lors de la suppression du titre : {e}")
        # Si vous utilisiez des sessions, il faudrait rollback en cas d'erreur
        # session.rollback()
        return False