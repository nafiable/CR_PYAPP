# Fichier: sqliteOperation/devise_operations.py

import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Définir le modèle de table pour SQLAlchemy (peut être remplacé par l'importation des schémas Pydantic si l'on utilise une approche ORM complète)
Base = declarative_base()

logger = logging.getLogger(__name__)

class Devise(Base):
    """
    Modèle SQLAlchemy pour la table 'Devise' en SQLite.
    """
    __tablename__ = 'Devise'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    nom = Column(String)
    idPays = Column(Integer)

# Note : Pour une utilisation correcte avec le reste du projet,
# il faudrait utiliser l'engine de connexion géré par la classe SQLiteConnection
# et potentiellement les modèles Pydantic pour la validation des données.
# Ces fonctions sont des exemples basiques.

def create_devise(connection, devise_data: dict):
    """
    Crée une nouvelle devise dans la base de données SQLite.

    Args:
        connection: Objet de connexion SQLAlchemy ou session.
        devise_data (dict): Dictionnaire contenant les données de la devise.

    Returns:
        dict: Les données de la devise créée, ou None en cas d'échec.
    """
    session = sessionmaker(bind=connection)()
    try:
        # Créer une nouvelle instance du modèle Devise avec les données fournies
        nouvelle_devise = Devise(
            code=devise_data.get('code'),
            nom=devise_data.get('nom'),
            idPays=devise_data.get('idPays')
        )

        session.add(nouvelle_devise)
        # Utiliser une transaction pour garantir l'atomicité
        # Note : session.commit() gère implicitement une transaction par défaut si aucune n'est active.
        # Pour une gestion plus explicite ou si vous utilisez session.begin(), cela serait géré différemment.
        # Ici, commit() est suffisant pour un simple insert.

        session.commit()
        session.refresh(nouvelle_devise)
        session.close()
        return {"id": nouvelle_devise.id, "code": nouvelle_devise.code, "nom": nouvelle_devise.nom, "idPays": nouvelle_devise.idPays}
    except Exception as e:
        logger.error(f"Erreur lors de la création de la devise : {e}")
        return None

def get_devise_by_id(connection, devise_id: int):
    """
    Récupère une devise par son ID depuis la base de données SQLite.

    Args:
        connection: Objet de connexion SQLAlchemy ou session.
        devise_id (int): L'ID de la devise à récupérer.

    Returns:
        dict: Les données de la devise, ou None si non trouvée.
    """
    session = sessionmaker(bind=connection)()
    try:
        session = Session()
        devise = session.query(Devise).filter_by(id=devise_id).first()
        session.close()
        if devise:
            logger.info(f"Devise trouvée avec l'ID {devise_id}")
            return {"id": devise.id, "code": devise.code, "nom": devise.nom, "idPays": devise.idPays}
        logger.info(f"Aucune devise trouvée avec l'ID {devise_id}")
        return None
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la devise avec l'ID {devise_id} : {e}")
        return None

def update_devise(connection, devise_id: int, devise_data: dict):
    """
    Met à jour une devise existante dans la base de données SQLite.

    Args:
        connection: Objet de connexion SQLAlchemy ou session.
        devise_id (int): L'ID de la devise à mettre à jour.
        devise_data (dict): Dictionnaire contenant les données à mettre à jour.

    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    session = sessionmaker(bind=connection)()
    try:
        session = Session()
        devise = session.query(Devise).filter_by(id=devise_id).first()
        logger.info(f"Tentative de mise à jour de la devise avec l'ID {devise_id}")
        if devise:
            # Mettre à jour les champs de la devise avec les données fournies
            for key, value in devise_data.items():
                # Vérifier si l'attribut existe sur le modèle avant de le définir
                logger.debug(f"Mise à jour du champ {key} avec la valeur {value} pour la devise {devise_id}")
                if hasattr(devise, key):
                setattr(devise, key, value)

            # Utiliser une transaction
            session.commit()
            session.close()
            return True
        logger.warning(f"Aucune devise trouvée avec l'ID {devise_id} pour la mise à jour.")
        session.close() # Fermer la session même si aucune devise n'est trouvée
        return False
    except Exception as e:
        session.rollback() # Annuler la transaction en cas d'erreur
        logger.error(f"Erreur lors de la mise à jour de la devise avec l'ID {devise_id} : {e}")
        return False

def delete_devise(connection, devise_id: int):
    """
    Supprime une devise de la base de données SQLite.

    Args:
        connection: Objet de connexion SQLAlchemy ou session.
        devise_id (int): L'ID de la devise à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    session = sessionmaker(bind=connection)()
    try:
        session = Session()
        devise = session.query(Devise).filter_by(id=devise_id).first()
        logger.info(f"Tentative de suppression de la devise avec l'ID {devise_id}")
        if devise:
            # Supprimer la devise trouvée
            session.delete(devise)
            # Utiliser une transaction
            session.commit()
            session.close()
            logger.info(f"Devise avec l'ID {devise_id} supprimée avec succès.")
            return True
        logger.warning(f"Aucune devise trouvée avec l'ID {devise_id} pour la suppression.")
        session.close() # Fermer la session même si aucune devise n'est trouvée
        return False
    except Exception as e:
        session.rollback() # Annuler la transaction en cas d'erreur
        logger.error(f"Erreur lors de la suppression de la devise avec l'ID {devise_id} : {e}")
        return False