from pydantic import BaseModel

class TypeActif1(BaseModel):
    """
    Modèle Pydantic pour l'objet TypeActif1.
    Représente un type principal d'actif.
    """
    id: int
    type: str