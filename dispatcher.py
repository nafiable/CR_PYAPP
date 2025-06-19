# dispatcher.py

import logging
import json
from typing import Dict, Any, Optional
from functools import wraps
from contextlib import asynccontextmanager

from fastapi import HTTPException
from constantes import const1
from database.connexionsqlServer import SQLServerConnection
from database.connexionsqlLiter import SQLiteConnection
from logic import fund_calculations, data_import_logic

logger = logging.getLogger(__name__)

class DispatcherError(Exception):
    """Exception personnalisée pour les erreurs du dispatcher."""
    pass

def validate_payload(required_fields: list):
    """
    Décorateur pour valider les champs requis dans le payload.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(payload: Dict[str, Any], *args, **kwargs):
            missing_fields = [field for field in required_fields if field not in payload]
            if missing_fields:
                raise ValueError(f"Champs manquants dans le payload: {', '.join(missing_fields)}")
            return await func(payload, *args, **kwargs)
        return wrapper
    return decorator

@asynccontextmanager
async def get_db_connection():
    """
    Gestionnaire de contexte pour la connexion à la base de données.
    """
    if not hasattr(const1, 'ENV_TYPE'):
        const1.load_config()

    try:
        if const1.ENV_TYPE == 'development':
            from sqliteOperation import test_operations as db_operations
            connection = SQLiteConnection()
        else:
            from sqlserverOperation import test_operations as db_operations
            connection = SQLServerConnection()
        yield connection, db_operations
    finally:
        if connection:
            await connection.close()

class FunctionRegistry:
    """Registre des fonctions disponibles dans le dispatcher."""
    
    @staticmethod
    @validate_payload(['id', 'name'])
    async def insert_test_data(payload: Dict[str, Any], connection, db_operations):
        return await db_operations.insert_test_data(connection, payload['id'], payload['name'])

    @staticmethod
    @validate_payload(['fund_id', 'date'])
    async def calculate_fund_market_value(payload: Dict[str, Any], connection, db_operations):
        return await fund_calculations.calculate_market_value(
            payload['fund_id'],
            payload['date'],
            connection
        )

    @staticmethod
    @validate_payload(['remote_filepath', 'local_filepath', 'target_table_name'])
    async def import_sftp_data(payload: Dict[str, Any], connection, db_operations):
        await data_import_logic.import_data_from_sftp(
            payload['remote_filepath'],
            payload['local_filepath'],
            payload['target_table_name']
        )
        return {"message": "Importation SFTP terminée avec succès"}

# Mapping explicite entre noms d'API et fonctions réelles
FUNCTION_NAME_MAPPING = {
    # "nom_recu": "nom_interne"
    "insert_test_data": "insert_test_data",
    "calculate_fund_market_value": "calculate_fund_market_value",
    "import_sftp_data": "import_sftp_data",
    # Ajoutez ici d'autres alias ou mappings personnalisés
    # "ajouter_gestionnaire": "insert_test_data",
}

async def dispatch_request_mapped(function_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Version alternative du dispatcher utilisant un mapping explicite entre noms d'API et fonctions réelles.
    """
    logger.info(f"Traitement de la requête (mapping) pour la fonction: {function_name}")
    logger.debug(f"Payload reçu: {json.dumps(payload or {}, indent=2)}")

    # Chercher le nom réel de la fonction
    real_function = FUNCTION_NAME_MAPPING.get(function_name)
    if not real_function or not hasattr(FunctionRegistry, real_function):
        raise HTTPException(
            status_code=404,
            detail=f"Fonction non trouvée (mapping): {function_name}"
        )

    try:
        async with get_db_connection() as (connection, db_operations):
            handler = getattr(FunctionRegistry, real_function)
            result = await handler(payload or {}, connection, db_operations)
            return {
                "status": "success",
                "data": result
            }
    except ValueError as e:
        logger.warning(f"Erreur de validation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except DispatcherError as e:
        logger.error(f"Erreur du dispatcher: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne s'est produite (mapping)"
        )
