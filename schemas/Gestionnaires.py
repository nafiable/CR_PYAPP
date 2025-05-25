from pydantic import BaseModel

class Gestionnaire(BaseModel):
    """
    Modèle Pydantic pour l'objet Gestionnaire.
    """
    id: int
    nom: str
    code: str
    tel: str
    contactPrincipal: str
    email: str
