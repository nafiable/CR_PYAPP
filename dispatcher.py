# dispatcher.py

import json
from constantes import const1
from database.connexionsqlServer import SQLServerConnection
from database.connexionsqlLiter import SQLiteConnection
from logic import fund_calculations, data_import_logic


async def dispatch_request(function_name: str, payload: dict):
    """
    Distribue les requêtes entrantes vers les fonctions appropriées.

    Args:
        function_name (str): Le nom de la fonction logique à exécuter.
        payload (dict): La charge utile au format JSON pour la fonction.

    Returns:
        dict: La réponse au format JSON.
    """
    # Charger les constantes si elles ne l'ont pas déjà été
    if not hasattr(const1, 'ENV_TYPE'):
        const1.load_config()

    print(f"Requête reçue pour la fonction : {function_name}")
    print(f"Charge utile : {json.dumps(payload, indent=2)}")

    # Logique de dispatching à ajouter ici
    if const1.ENV_TYPE == 'development':
        from sqliteOperation import test_operations as db_operations
        connexion = SQLiteConnection()
    else:
        from sqlserverOperation import test_operations as db_operations
        connexion = SQLServerConnection()

    response = {}

    try:
        if function_name == 'insert_test_data':
            # Supposer que le payload contient 'id' et 'name' pour insert_test_data
            result = db_operations.insert_test_data(connexion, payload.get('id'), payload.get('name'))
            response = {"status": "success", "result": result}
        elif function_name == 'calculate_fund_market_value':
            # Vérifier que le payload contient les clés nécessaires
            fund_id = payload.get('fund_id')
            date = payload.get('date')
            if fund_id is None or date is None:
                raise ValueError("Payload doit contenir 'fund_id' et 'date'")

            # Appeler la fonction de logique métier
            result = fund_calculations.calculate_market_value(fund_id, date, connexion)
            response = {"status": "success", "result": result}
        elif function_name == 'import_sftp_data':
            # Vérifier que le payload contient les clés nécessaires
 remote_filepath = payload.get('remote_filepath')
 local_filepath = payload.get('local_filepath')
            target_table_name = payload.get('target_table_name')
            if remote_filepath is None or local_filepath is None or target_table_name is None:
 raise ValueError("Payload doit contenir 'remote_filepath', 'local_filepath' et 'target_table_name'")

            # Appeler la fonction d'importation de données SFTP
 await data_import_logic.import_data_from_sftp(remote_filepath, local_filepath, target_table_name)
            response = {"status": "success", "message": "Importation SFTP initiée."}
        else:
            response = {"status": "error", "message": f"Fonction non trouvée: {function_name}"}
    except Exception as e:
        response = {"status": "error", "message": f"Une erreur est survenue lors de l'exécution de la fonction {function_name}: {str(e)}"}

    return response
