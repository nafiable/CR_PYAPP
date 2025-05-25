from pydantic import BaseModel
from datetime import date

class CompositionIndice(BaseModel):
    """
    Modèle Pydantic représentant la composition d'un indice à une date donnée.
    """
    date: date
    id_indice: int
    id_titre: int
    quantite: float
    prix: float
    valeur_marchande: float
    dividende: float