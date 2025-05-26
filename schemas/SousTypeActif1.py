from pydantic import BaseModel

import logging
logger = logging.getLogger(__name__)

class SousTypeActif1(BaseModel):
    """
    Modèle Pydantic pour représenter un SousTypeActif1.
    """
    id: int
    idTypeAcif1: int  # Clé étrangère vers TypeActif1
    nom: str
