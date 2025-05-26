# schemas/Devise.py

from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# Modèle Pydantic pour l'objet Devise
class Devise(BaseModel):
    """
    Représente une devise.
    """
    id: int
    code: str
    nom: str
    idPays: int