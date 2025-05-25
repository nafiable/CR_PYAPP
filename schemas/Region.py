# Modèle Pydantic pour l'objet Region

from pydantic import BaseModel

class Region(BaseModel):
    """
    Représente une région géographique.
    """
    id: int
    code: str
    nom: str