from pydantic import BaseModel

import logging
logger = logging.getLogger(__name__)

class Secteur(BaseModel):
    """
    Modèle Pydantic pour l'objet Secteur.
    """
    id: int
    codeGics: str
    codeBics: str
    nom: str