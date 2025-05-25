from sqlalchemy.orm import Session
from sqlalchemy import text, exc
from schemas.TypeActif1 import TypeActif1  # Assurez-vous que l'importation est correcte

def create_typeactif1(connection: Session, typeactif1_data: TypeActif1):
    """
    Insère une nouvelle entrée dans la table TypeActif1.
    Gère les exceptions et utilise des transactions.

    Args:
        connection: La session SQLAlchemy connectée à la base de données SQL Server.
        typeactif1_data: Les données du TypeActif1 à créer (modèle Pydantic TypeActif1).

    Returns:
        True si la création est réussie, False sinon.
    """
    try:
        # Convertir le modèle Pydantic en dictionnaire pour l'insertion
        data_to_insert = typeactif1_data.model_dump(exclude_unset=True) # Exclure les champs non définis

        with connection.begin(): # Démarre une transaction
            # Construire la requête SQL d'insertion
            # Utiliser des paramètres pour éviter les injections SQL
            query = text("INSERT INTO TypeActif1 (id, type) VALUES (:id, :type)")

            # Exécuter la requête avec les paramètres
            connection.execute(query, data_to_insert)
            # La transaction est automatiquement commitée si aucune exception n'est levée
        print(f"TypeActif1 créé avec succès: ID {typeactif1_data.id}")
        return True
    except exc.IntegrityError as e:
        # Gérer les erreurs d'intégrité (ex: clé primaire dupliquée)
        print(f"Erreur d'intégrité lors de la création du TypeActif1 : {e}")
        # La transaction est automatiquement rollbackée en cas d'exception dans le bloc 'with'
        return False
    except Exception as e: # Gérer les autres exceptions potentielles
        print(f"Erreur lors de la création du TypeActif1 : {e}")
        return False

def get_typeactif1_by_id(connection: Session, typeactif1_id: int):
    """
    Récupère une entrée de la table TypeActif1 par son ID.
    Gère les exceptions.

    Args:
        connection: La session SQLAlchemy connectée à la base de données SQL Server.
        typeactif1_id: L'ID du TypeActif1 à récupérer.

    Returns:
        Un dictionnaire représentant le TypeActif1 s'il est trouvé, None sinon.
    """
    try:
        # Pas besoin de transaction pour une simple lecture
        query = text("SELECT id, type FROM TypeActif1 WHERE id = :typeactif1_id")
        result = connection.execute(query, {"typeactif1_id": typeactif1_id}).fetchone()        

        if result:            
            # Retourne un dictionnaire mappant les noms de colonnes aux valeurs
            return {col: result[col] for col in result.keys()}
        else:
            return None # Aucune région trouvée avec cet ID
    except Exception as e: # Gérer les autres exceptions potentielles
        print(f"Erreur lors de la récupération du TypeActif1 : {e}")
        return None

def update_typeactif1(connection: Session, typeactif1_id: int, typeactif1_data: dict):
    """
    Met à jour une entrée existante dans la table TypeActif1.
    Gère les exceptions et utilise des transactions.

    Args:
        connection: La session SQLAlchemy connectée à la base de données SQL Server.
        typeactif1_id: L'ID du TypeActif1 à mettre à jour.
        typeactif1_data: Les données à mettre à jour (dictionnaire ou modèle Pydantic, nous utiliserons un dict pour la flexibilité de la mise à jour partielle).

    Returns:
        True si la mise à jour est réussie, False sinon.
    """
    if not typeactif1_data:
        print("Aucune donnée de mise à jour fournie pour TypeActif1.")
        return False

    try:
        with connection.begin(): # Démarre une transaction
            # Construire la partie SET de la requête SQL dynamiquement
            set_clauses = ', '.join([f"{key} = :{key}" for key in typeactif1_data.keys()])

            if not set_clauses:
                print(f"Aucun champ valide trouvé dans les données de mise à jour pour TypeActif1 ID {typeactif1_id}.")
                return False

            query = text(f"UPDATE TypeActif1 SET {set_clauses} WHERE id = :typeactif1_id")

            # Ajouter l'ID à mettre à jour aux paramètres
            params = typeactif1_data.copy()
            params["typeactif1_id"] = typeactif1_id

            result = connection.execute(query, params)
            # La transaction est automatiquement commitée
        if result.rowcount > 0:
            print(f"TypeActif1 avec ID {typeactif1_id} mis à jour avec succès.")
            return True
        else:
            print(f"Aucun TypeActif1 trouvé avec l'ID {typeactif1_id} pour mise à jour.")
            return False
    except Exception as e: # Gérer les autres exceptions potentielles
        print(f"Erreur lors de la mise à jour du TypeActif1 avec ID {typeactif1_id}: {e}")
        return False

def delete_typeactif1(connection: Session, typeactif1_id: int):
    """
    Supprime une entrée de la table TypeActif1 par son ID.
    Gère les exceptions et utilise des transactions.

    Args:
        connection: La session SQLAlchemy connectée à la base de données SQL Server.
        typeactif1_id: L'ID du TypeActif1 à supprimer.

    Returns:
        True si la suppression est réussie, False sinon.
    """
    try:
        with connection.begin(): # Démarre une transaction
            query = text("DELETE FROM TypeActif1 WHERE id = :typeactif1_id")
            result = connection.execute(query, {"typeactif1_id": typeactif1_id})
            # La transaction est automatiquement commitée
        if result.rowcount > 0:
            print(f"TypeActif1 avec ID {typeactif1_id} supprimé avec succès.")
            return True
        else:
            print(f"Aucun TypeActif1 trouvé avec l'ID {typeactif1_id} pour suppression.")
            return False
    except Exception as e: # Gérer les autres exceptions potentielles
        print(f"Erreur lors de la suppression du TypeActif1 avec ID {typeactif1_id}: {e}")
        return False