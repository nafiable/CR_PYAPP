# Fichier : schemas/Indice.py

from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Indice(BaseModel):
    """
    Modèle Pydantic pour représenter un Indice.
    """
    id: int
    nom: str