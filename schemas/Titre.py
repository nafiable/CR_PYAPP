# Fichier : schemas/Titre.py

from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Titre(BaseModel):
    """
    Modèle Pydantic pour représenter un Titre.
    """
    id: int
    nom: str
    cusip: str
    isin: str
    ticker: str
    emetteur: str
    idTypeTitre1: int
    idSousTypeTitre1: int
    idTypeTitre2: int
    idSecteur: int
    idClassification1: int
    idSousClassification1: int
    classification2: str
    idNotation: int
    idPays: int