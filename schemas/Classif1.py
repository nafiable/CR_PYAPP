import logging

logger = logging.getLogger(__name__)
from pydantic import BaseModel

class Classif1(BaseModel):
    """
    Modèle Pydantic pour représenter un objet Classif1.
    """
    id: int
    nom: str