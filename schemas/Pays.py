from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Pays(BaseModel):
    """
    Modèle Pydantic pour l'objet Pays.
    Représente un pays avec ses informations associées.
    """
    id: int
    code: str
    nom: str
    idRegion: int  # Clé étrangère vers la table Region
    continent: str
    idDevise: int  # Clé étrangère vers la table Devise