# sqlserverOperation/compositionportefeuillegestionnaire_operations.py

from sqlalchemy import text

def create_composition(connection, composition_data):
    """
    Insère une nouvelle composition de portefeuille par gestionnaire dans la base de données SQL Server.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        composition_data (dict ou schemas.CompositionPortefeuilleGestionnaire): Les données de composition.

    Returns:
        bool: True si l'insertion a réussi, False sinon.
    """
    try:
        with connection.connect() as conn:
            # Assurez-vous que composition_data est un dictionnaire
            if hasattr(composition_data, 'model_dump'):
                data_to_insert = composition_data.model_dump()
            else:
                data_to_insert = composition_data

            # Construction de la requête SQL d'insertion
            columns = ', '.join(data_to_insert.keys())
            values_placeholders = ', '.join([f':{key}' for key in data_to_insert.keys()])
            query = text(f"INSERT INTO CompositionPortefeuilleGestionnaire ({columns}) VALUES ({values_placeholders})")

            conn.execute(query, data_to_insert)
            conn.commit()
            return True
    except Exception as e:
        print(f"Erreur lors de la création de la composition de portefeuille par gestionnaire: {e}")
        return False

def get_composition(connection, fonds_id: int, gestionnaire_id: int, date):
    """
    Récupère une composition de portefeuille par gestionnaire spécifique par ID de fonds, gestionnaire et date.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        fonds_id (int): L'ID du fonds (portefeuille).
        gestionnaire_id (int): L'ID du gestionnaire.
        date: La date de la composition (peut être un objet date, datetime ou une chaîne compatible SQL).

    Returns:
        dict ou None: Les données de la composition si trouvée, sinon None.
    """
    try:
        with connection.connect() as conn:
            query = text("SELECT * FROM CompositionPortefeuilleGestionnaire WHERE id_fonds = :fonds_id AND id_gestionnaire = :gestionnaire_id AND date = :date")
            result = conn.execute(query, {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date": date}).fetchone()
            if result:
                # Convertir le résultat en dictionnaire
                return dict(result._mapping)
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération de la composition de portefeuille par gestionnaire: {e}")
        return None

def update_composition(connection, fonds_id: int, gestionnaire_id: int, date, composition_data):
    """
    Met à jour une composition de portefeuille par gestionnaire existante.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        fonds_id (int): L'ID du fonds (portefeuille).
        gestionnaire_id (int): L'ID du gestionnaire.
        date: La date de la composition.
        composition_data (dict ou schemas.CompositionPortefeuilleGestionnaire): Les données de composition à mettre à jour.

    Returns:
        bool: True si la mise à jour a réussi, False sinon.
    """
    try:
        with connection.connect() as conn:
            # Assurez-vous que composition_data est un dictionnaire
            if hasattr(composition_data, 'model_dump'):
                data_to_update = composition_data.model_dump()
            else:
                data_to_update = composition_data

            # Construction de la requête SQL de mise à jour
            set_clauses = ', '.join([f"{key} = :{key}" for key in data_to_update.keys()])
            query = text(f"UPDATE CompositionPortefeuilleGestionnaire SET {set_clauses} WHERE id_fonds = :fonds_id AND id_gestionnaire = :gestionnaire_id AND date = :date")

            params = data_to_update
            params["fonds_id"] = fonds_id
            params["gestionnaire_id"] = gestionnaire_id
            params["date"] = date

            result = conn.execute(query, params)
 # Conn.commit() n'est pas nécessaire ici si l'engine est utilisé dans un bloc 'with'
 return result.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la composition de portefeuille par gestionnaire: {e}")
        return False

def delete_composition(connection, fonds_id: int, gestionnaire_id: int, date):
    """
    Supprime une composition de portefeuille par gestionnaire spécifique par ID de fonds, gestionnaire et date.

    Args:
        connection: L'objet de connexion SQLAlchemy.
        fonds_id (int): L'ID du fonds (portefeuille).
        gestionnaire_id (int): L'ID du gestionnaire.
        date: La date de la composition.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    try:
        with connection.connect() as conn:
            query = text("DELETE FROM CompositionPortefeuilleGestionnaire WHERE id_fonds = :fonds_id AND id_gestionnaire = :gestionnaire_id AND date = :date")
            result = conn.execute(query, {"fonds_id": fonds_id, "gestionnaire_id": gestionnaire_id, "date": date})
            conn.commit()
            return result.rowcount > 0
    except Exception as e:
        print(f"Erreur lors de la suppression de la composition de portefeuille par gestionnaire: {e}")
        return False

# Exemple d'utilisation (pour les tests unitaires ou l'intégration)
if __name__ == '__main__':
    # Cet exemple nécessite une connexion SQL Server fonctionnelle
    # et une table CompositionPortefeuilleGestionnaire existante.
    # Remplacez les informations de connexion par les vôtres.
    from constantes.const1 import load_config, BD_SERVER, BD_NAME, BD_USER, BD_PASSWORD
    from database.connexionsqlServer import SQLServerConnection
    from datetime import date

    load_config() # Charger la configuration depuis config.env

    # Créer une instance de connexion (assurez-vous que les constantes sont définies)
    db_connection_manager = None
    try:
        db_connection_manager = SQLServerConnection()
        connection = db_connection_manager.get_engine()

        # Exemple de données de composition
        new_composition_data = {
            "date": date.today(),
            "id_fonds": 1,
            "id_gestionnaire": 1,
            "id_Titre": 101,
            "id_devise": 1,
            "id_pays": 1,
            "quantite": 100.5,
            "prix": 50.25,
            "valeur_marchande": 5050.125,
            "accrued": 10.0,
            "dividende": 5.0
        }

        # Créer une nouvelle composition
        print("Création d'une composition...")
        if create_composition(connection, new_composition_data):
            print("Composition créée avec succès.")
        else:
            print("Échec de la création de la composition.")

        # Récupérer la composition créée
        print("\nRécupération de la composition...")
        retrieved_composition = get_composition(connection, 1, 1, date.today())
        if retrieved_composition:
            print("Composition récupérée:", retrieved_composition)
        else:
            print("Composition non trouvée.")

        # Mettre à jour la composition
        print("\nMise à jour de la composition...")
        update_data = {"prix": 55.0, "valeur_marchande": 5527.5}
        if update_composition(connection, 1, 1, date.today(), update_data):
            print("Composition mise à jour avec succès.")
        else:
            print("Échec de la mise à jour de la composition.")

        # Récupérer la composition mise à jour
        print("\nRécupération de la composition mise à jour...")
        retrieved_composition_updated = get_composition(connection, 1, 1, date.today())
        if retrieved_composition_updated:
            print("Composition mise à jour récupérée:", retrieved_composition_updated)
        else:
            print("Composition non trouvée après mise à jour.")

        # Supprimer la composition
        print("\nSuppression de la composition...")
        if delete_composition(connection, 1, 1, date.today()):
            print("Composition supprimée avec succès.")
        else:
            print("Échec de la suppression de la composition.")

        # Tenter de récupérer la composition supprimée
        print("\nTentative de récupération de la composition supprimée...")
        retrieved_composition_deleted = get_composition(connection, 1, 1, date.today())
        if retrieved_composition_deleted:
            print("Composition supprimée toujours trouvée (erreur).")
        else:
            print("Composition supprimée non trouvée (succès).")

    except Exception as e:
        print(f"Erreur générale dans l'exemple: {e}")
    finally:
        if db_connection_manager:
            db_connection_manager.close_connection()