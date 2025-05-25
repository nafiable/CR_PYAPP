# schemas/Devise.py

from pydantic import BaseModel

# Modèle Pydantic pour l'objet Devise
class Devise(BaseModel):
    """
    Représente une devise.
    """
    id: int
    code: str
    nom: str
    idPays: int