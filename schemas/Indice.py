# Fichier : schemas/Indice.py

from pydantic import BaseModel

class Indice(BaseModel):
    """
    Modèle Pydantic pour représenter un Indice.
    """
    id: int
    nom: str