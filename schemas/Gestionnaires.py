from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Gestionnaire(BaseModel):
    """
    Modèle Pydantic pour l'objet Gestionnaire.
    """
    id: int
    nom: str
    code: str
    tel: str
    contactPrincipal: str
    email: str
