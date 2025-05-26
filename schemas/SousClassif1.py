from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class SousClassif1(BaseModel):
    """
    Modèle Pydantic pour l'objet SousClassif1.
    Représente une sous-classification principale.
    """
    id: int
    idClassif1: int  # Clé étrangère vers Classif1
    nom: str