"""
Modèles des entités principales de l'application.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel, BaseCodeNom
import enum

class TypeFonds(enum.Enum):
    """Types de fonds disponibles."""
    SIMPLE = "simple"
    PORTEFEUILLE = "portefeuille"

class Gestionnaire(BaseCodeNom):
    """Modèle pour les gestionnaires de fonds."""
    __tablename__ = "gestionnaire"
    
    tel = Column(String(20))
    contact_principal = Column(String(100))
    email = Column(String(255))
    
    # Relations
    fonds = relationship("FondsGestionnaire", back_populates="gestionnaire")

class Region(BaseCodeNom):
    """Modèle pour les régions."""
    __tablename__ = "region1"
    
    # Relations
    pays = relationship("Pays", back_populates="region")

class Pays(BaseCodeNom):
    """Modèle pour les pays."""
    __tablename__ = "pays"
    
    id_region = Column(Integer, ForeignKey("region1.id"), nullable=False)
    continent = Column(String(50))
    id_devise = Column(Integer, ForeignKey("devise.id"), nullable=False)
    
    # Relations
    region = relationship("Region", back_populates="pays")
    devise = relationship("Devise", back_populates="pays")

class Devise(BaseCodeNom):
    """Modèle pour les devises."""
    __tablename__ = "devise"
    
    # Relations
    pays = relationship("Pays", back_populates="devise")

class Secteur(BaseCodeNom):
    """Modèle pour les secteurs."""
    __tablename__ = "secteur"
    
    code_gics = Column(String(50))
    code_bics = Column(String(50))

class TypeActif(BaseCodeNom):
    """Modèle pour les types d'actifs."""
    __tablename__ = "type_actif1"
    
    type = Column(String(50))
    
    # Relations
    sous_types = relationship("SousTypeActif", back_populates="type_actif")

class SousTypeActif(BaseCodeNom):
    """Modèle pour les sous-types d'actifs."""
    __tablename__ = "sous_type_actif1"
    
    id_type_actif = Column(Integer, ForeignKey("type_actif1.id"), nullable=False)
    
    # Relations
    type_actif = relationship("TypeActif", back_populates="sous_types")

class Classif(BaseCodeNom):
    """Modèle pour les classifications."""
    __tablename__ = "classif1"
    
    # Relations
    sous_classifs = relationship("SousClassif", back_populates="classif")

class SousClassif(BaseCodeNom):
    """Modèle pour les sous-classifications."""
    __tablename__ = "sous_classif1"
    
    id_classif = Column(Integer, ForeignKey("classif1.id"), nullable=False)
    
    # Relations
    classif = relationship("Classif", back_populates="sous_classifs")

class Titre(BaseCodeNom):
    """Modèle pour les titres."""
    __tablename__ = "titre"
    
    cusip = Column(String(50), unique=True)
    isin = Column(String(50), unique=True)
    ticker = Column(String(50))
    emetteur = Column(String(255))
    id_type_actif = Column(Integer, ForeignKey("type_actif1.id"))
    id_sous_type_actif = Column(Integer, ForeignKey("sous_type_actif1.id"))
    id_secteur = Column(Integer, ForeignKey("secteur.id"))
    id_classif = Column(Integer, ForeignKey("classif1.id"))
    id_sous_classif = Column(Integer, ForeignKey("sous_classif1.id"))
    id_pays = Column(Integer, ForeignKey("pays.id"))
    
    # Relations
    type_actif = relationship("TypeActif")
    sous_type_actif = relationship("SousTypeActif")
    secteur = relationship("Secteur")
    classif = relationship("Classif")
    sous_classif = relationship("SousClassif")
    pays = relationship("Pays")

class Indice(BaseCodeNom):
    """Modèle pour les indices."""
    __tablename__ = "indice"
    
    # Relations
    fonds = relationship("FondsIndice", back_populates="indice")
    compositions = relationship("CompositionIndice", back_populates="indice")

class Fonds(BaseCodeNom):
    """Modèle pour les fonds."""
    __tablename__ = "fonds"
    
    type_fonds = Column(Enum(TypeFonds), nullable=False)
    
    # Relations
    gestionnaires = relationship("FondsGestionnaire", back_populates="fonds")
    indices = relationship("FondsIndice", back_populates="fonds")
    compositions = relationship("CompositionFonds", back_populates="fonds")

# Tables de liaison
class FondsGestionnaire(BaseModel):
    """Table de liaison entre fonds et gestionnaires."""
    __tablename__ = "fonds_gestionnaire"
    
    id_fonds = Column(Integer, ForeignKey("fonds.id"), primary_key=True)
    id_gestionnaire = Column(Integer, ForeignKey("gestionnaire.id"), primary_key=True)
    
    # Relations
    fonds = relationship("Fonds", back_populates="gestionnaires")
    gestionnaire = relationship("Gestionnaire", back_populates="fonds")

class FondsIndice(BaseModel):
    """Table de liaison entre fonds et indices."""
    __tablename__ = "fonds_indice"
    
    id_fonds = Column(Integer, ForeignKey("fonds.id"), primary_key=True)
    id_indice = Column(Integer, ForeignKey("indice.id"), primary_key=True)
    
    # Relations
    fonds = relationship("Fonds", back_populates="indices")
    indice = relationship("Indice", back_populates="fonds")

class CompositionBase(BaseModel):
    """Classe de base pour les compositions."""
    __abstract__ = True
    
    date = Column(Date, nullable=False)
    id_titre = Column(Integer, ForeignKey("titre.id"), nullable=False)
    id_devise = Column(Integer, ForeignKey("devise.id"), nullable=False)
    id_pays = Column(Integer, ForeignKey("pays.id"), nullable=False)
    quantite = Column(Float)
    prix = Column(Float)
    valeur_marchande = Column(Float)
    accrued = Column(Float)
    dividende = Column(Float)

class CompositionFonds(CompositionBase):
    """Modèle pour la composition des fonds."""
    __tablename__ = "composition_fonds_gestionnaire"
    
    id_fonds = Column(Integer, ForeignKey("fonds.id"), nullable=False)
    id_gestionnaire = Column(Integer, ForeignKey("gestionnaire.id"), nullable=False)
    
    # Relations
    fonds = relationship("Fonds", back_populates="compositions")
    titre = relationship("Titre")
    devise = relationship("Devise")
    pays = relationship("Pays")
    gestionnaire = relationship("Gestionnaire")

class CompositionPortefeuille(CompositionBase):
    """Modèle pour la composition des portefeuilles."""
    __tablename__ = "composition_portefeuille_gestionnaire"
    
    id_portefeuille = Column(Integer, ForeignKey("fonds.id"), nullable=False)
    id_gestionnaire = Column(Integer, ForeignKey("gestionnaire.id"), nullable=False)
    
    # Relations
    portefeuille = relationship("Fonds")
    titre = relationship("Titre")
    devise = relationship("Devise")
    pays = relationship("Pays")
    gestionnaire = relationship("Gestionnaire")

class CompositionIndice(CompositionBase):
    """Modèle pour la composition des indices."""
    __tablename__ = "composition_indice"
    
    id_indice = Column(Integer, ForeignKey("indice.id"), nullable=False)
    
    # Relations
    indice = relationship("Indice", back_populates="compositions")
    titre = relationship("Titre")
    devise = relationship("Devise")
    pays = relationship("Pays") 