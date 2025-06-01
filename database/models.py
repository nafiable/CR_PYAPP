"""
Module des modèles SQLAlchemy.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BaseModel(Base):
    """Classe de base pour tous les modèles."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)
    nom = Column(String(100))
    description = Column(String(500), nullable=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Gestionnaire(BaseModel):
    """Modèle pour les gestionnaires."""
    
    __tablename__ = "gestionnaire"
    
    tel = Column(String(20))
    contact_principal = Column(String(100))
    email = Column(String(100))
    fonds = relationship("Fonds", secondary="gestionnaire_fonds", back_populates="gestionnaires")

class Region(BaseModel):
    """Modèle pour les régions."""
    
    __tablename__ = "region"
    
    pays = relationship("Pays", back_populates="region")

class Pays(BaseModel):
    """Modèle pour les pays."""
    
    __tablename__ = "pays"
    
    continent = Column(String(50))
    id_region = Column(Integer, ForeignKey("region.id"))
    id_devise = Column(Integer, ForeignKey("devise.id"))
    
    region = relationship("Region", back_populates="pays")
    devise = relationship("Devise", back_populates="pays")

class Devise(BaseModel):
    """Modèle pour les devises."""
    
    __tablename__ = "devise"
    
    pays = relationship("Pays", back_populates="devise")

class Secteur(BaseModel):
    """Modèle pour les secteurs."""
    
    __tablename__ = "secteur"
    
    code_gics = Column(String(10))
    code_bics = Column(String(10))

class TypeActif(BaseModel):
    """Modèle pour les types d'actifs."""
    
    __tablename__ = "type_actif"
    
    type = Column(String(50))
    sous_types = relationship("SousTypeActif", back_populates="type_actif")

class SousTypeActif(BaseModel):
    """Modèle pour les sous-types d'actifs."""
    
    __tablename__ = "sous_type_actif"
    
    id_type_actif = Column(Integer, ForeignKey("type_actif.id"))
    type_actif = relationship("TypeActif", back_populates="sous_types")

class Classif(BaseModel):
    """Modèle pour les classifications."""
    
    __tablename__ = "classif"
    
    sous_classifs = relationship("SousClassif", back_populates="classif")

class SousClassif(BaseModel):
    """Modèle pour les sous-classifications."""
    
    __tablename__ = "sous_classif"
    
    id_classif = Column(Integer, ForeignKey("classif.id"))
    classif = relationship("Classif", back_populates="sous_classifs")

class Titre(BaseModel):
    """Modèle pour les titres."""
    
    __tablename__ = "titre"
    
    cusip = Column(String(9))
    isin = Column(String(12))
    ticker = Column(String(20))
    emetteur = Column(String(100))
    id_type_actif = Column(Integer, ForeignKey("type_actif.id"))
    id_sous_type_actif = Column(Integer, ForeignKey("sous_type_actif.id"))
    id_secteur = Column(Integer, ForeignKey("secteur.id"))
    id_classif = Column(Integer, ForeignKey("classif.id"))
    id_sous_classif = Column(Integer, ForeignKey("sous_classif.id"))
    id_pays = Column(Integer, ForeignKey("pays.id"))

class Indice(BaseModel):
    """Modèle pour les indices."""
    
    __tablename__ = "indice"

class Fonds(BaseModel):
    """Modèle pour les fonds."""
    
    __tablename__ = "fonds"
    
    type_fonds = Column(String(20))  # 'simple' ou 'portefeuille'
    gestionnaires = relationship("Gestionnaire", secondary="gestionnaire_fonds", back_populates="fonds")
    indices = relationship("Indice", secondary="fonds_indice")

# Tables de liaison
class GestionnaireFonds(Base):
    """Table de liaison entre gestionnaires et fonds."""
    
    __tablename__ = "gestionnaire_fonds"
    
    id_gestionnaire = Column(Integer, ForeignKey("gestionnaire.id"), primary_key=True)
    id_fonds = Column(Integer, ForeignKey("fonds.id"), primary_key=True)

class FondsIndice(Base):
    """Table de liaison entre fonds et indices."""
    
    __tablename__ = "fonds_indice"
    
    id_fonds = Column(Integer, ForeignKey("fonds.id"), primary_key=True)
    id_indice = Column(Integer, ForeignKey("indice.id"), primary_key=True)

class CompositionFonds(Base):
    """Modèle pour la composition des fonds."""
    
    __tablename__ = "composition_fonds"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    id_fonds = Column(Integer, ForeignKey("fonds.id"))
    id_gestionnaire = Column(Integer, ForeignKey("gestionnaire.id"))
    id_titre = Column(Integer, ForeignKey("titre.id"))
    id_devise = Column(Integer, ForeignKey("devise.id"))
    id_pays = Column(Integer, ForeignKey("pays.id"))
    quantite = Column(Float)
    prix = Column(Float)
    valeur_marchande = Column(Float)
    accrued = Column(Float)
    dividende = Column(Float)

class CompositionPortefeuille(Base):
    """Modèle pour la composition des portefeuilles."""
    
    __tablename__ = "composition_portefeuille"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    id_portefeuille = Column(Integer, ForeignKey("fonds.id"))
    id_gestionnaire = Column(Integer, ForeignKey("gestionnaire.id"))
    id_titre = Column(Integer, ForeignKey("titre.id"))
    id_devise = Column(Integer, ForeignKey("devise.id"))
    id_pays = Column(Integer, ForeignKey("pays.id"))
    quantite = Column(Float)
    prix = Column(Float)
    valeur_marchande = Column(Float)
    accrued = Column(Float)
    dividende = Column(Float)

class CompositionIndice(Base):
    """Modèle pour la composition des indices."""
    
    __tablename__ = "composition_indice"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    id_indice = Column(Integer, ForeignKey("indice.id"))
    id_titre = Column(Integer, ForeignKey("titre.id"))
    id_devise = Column(Integer, ForeignKey("devise.id"))
    id_pays = Column(Integer, ForeignKey("pays.id"))
    quantite = Column(Float)
    prix = Column(Float)
    valeur_marchande = Column(Float)
    dividende = Column(Float) 