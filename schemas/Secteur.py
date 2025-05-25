from pydantic import BaseModel

class Secteur(BaseModel):
    """
    Modèle Pydantic pour l'objet Secteur.
    """
    id: int
    codeGics: str
    codeBics: str
    nom: str