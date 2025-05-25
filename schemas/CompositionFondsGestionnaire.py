from pydantic import BaseModel
from datetime import date

class CompositionFondsGestionnaire(BaseModel):
    """
    Modèle Pydantic pour la composition d'un fonds géré par un gestionnaire à une date donnée.
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