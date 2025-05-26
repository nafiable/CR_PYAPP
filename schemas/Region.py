# Modèle Pydantic pour l'objet Region

from pydantic import BaseModel
import logging
logger = logging.getLogger(__name__)

class Region(BaseModel):
    """
    Représente une région géographique.
    """
    id: int
    code: str
    nom: str