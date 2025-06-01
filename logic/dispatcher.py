"""
Module de dispatch des appels de fonctions.
"""

import logging
from typing import Dict, Any, Callable
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Dictionnaire des fonctions disponibles
AVAILABLE_FUNCTIONS: Dict[str, Callable] = {}

def register_function(name: str) -> Callable:
    """
    Décorateur pour enregistrer une fonction dans le dispatcher.
    
    Args:
        name (str): Nom de la fonction à enregistrer
        
    Returns:
        Callable: Le décorateur
    """
    def decorator(func: Callable) -> Callable:
        AVAILABLE_FUNCTIONS[name] = func
        logger.info(f"Fonction {name} enregistrée dans le dispatcher")
        return func
    return decorator

async def dispatch_request(function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch une requête vers la fonction appropriée.
    
    Args:
        function_name (str): Nom de la fonction à appeler
        payload (Dict[str, Any]): Données pour la fonction
        
    Returns:
        Dict[str, Any]: Résultat de la fonction
        
    Raises:
        HTTPException: Si la fonction n'existe pas ou en cas d'erreur
    """
    try:
        if function_name not in AVAILABLE_FUNCTIONS:
            raise HTTPException(
                status_code=404,
                detail=f"Fonction {function_name} non trouvée"
            )
            
        logger.info(f"Appel de la fonction {function_name}")
        logger.debug(f"Payload: {payload}")
        
        # Appel de la fonction
        result = await AVAILABLE_FUNCTIONS[function_name](**payload)
        
        logger.info(f"Fonction {function_name} exécutée avec succès")
        logger.debug(f"Résultat: {result}")
        
        return {
            "status": "success",
            "function": function_name,
            "result": result
        }
        
    except HTTPException as e:
        logger.warning(f"Erreur HTTP lors de l'appel de {function_name}: {str(e)}")
        raise
        
    except Exception as e:
        logger.error(
            f"Erreur lors de l'appel de {function_name}: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'exécution de {function_name}: {str(e)}"
        )

# Exemple d'utilisation du décorateur
@register_function("hello_world")
async def hello_world(name: str = "World") -> Dict[str, str]:
    """
    Fonction exemple.
    
    Args:
        name (str): Nom à saluer
        
    Returns:
        Dict[str, str]: Message de salutation
    """
    return {"message": f"Hello, {name}!"} 