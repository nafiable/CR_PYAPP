import logging
from pydantic import BaseModel
from datetime import date

logger = logging.getLogger(__name__)

class CompositionPortefeuilleGestionnaire(BaseModel):
    """
    Modèle Pydantic pour la composition d'un portefeuille par gestionnaire.
    """
    date: date
    id_fonds: int
    id_gestionnaire: int
    id_Titre: int
    id_devise: int
    id_pays: int
    quantite: float
    prix: float
    valeur_marchande: float
    accrued: float
    dividende: float