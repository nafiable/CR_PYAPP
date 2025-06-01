"""
Module pour les opérations CRUD spécifiques aux entités.
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date

from .base_crud import BaseCRUD
from database.models import (
    Gestionnaire, Region, Pays, Devise, Secteur,
    TypeActif, SousTypeActif, Classif, SousClassif,
    Titre, Indice, Fonds, CompositionFonds,
    CompositionPortefeuille, CompositionIndice
)

logger = logging.getLogger(__name__)

class GestionnaireCRUD(BaseCRUD[Gestionnaire]):
    """CRUD pour les gestionnaires."""
    def __init__(self):
        super().__init__(Gestionnaire)

class RegionCRUD(BaseCRUD[Region]):
    """CRUD pour les régions."""
    def __init__(self):
        super().__init__(Region)

class PaysCRUD(BaseCRUD[Pays]):
    """CRUD pour les pays."""
    def __init__(self):
        super().__init__(Pays)
    
    async def get_by_region(self, db: Session, region_id: int) -> List[Pays]:
        """
        Récupère tous les pays d'une région.
        
        Args:
            db (Session): Session de base de données
            region_id (int): ID de la région
            
        Returns:
            List[Pays]: Liste des pays
        """
        try:
            pays = db.query(self.model).filter(self.model.id_region == region_id).all()
            logger.info(f"{len(pays)} pays trouvés pour la région {region_id}")
            return pays
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des pays de la région {region_id}: {str(e)}")
            raise

class DeviseCRUD(BaseCRUD[Devise]):
    """CRUD pour les devises."""
    def __init__(self):
        super().__init__(Devise)

class SecteurCRUD(BaseCRUD[Secteur]):
    """CRUD pour les secteurs."""
    def __init__(self):
        super().__init__(Secteur)
    
    async def get_by_code_gics(self, db: Session, code_gics: str) -> Optional[Secteur]:
        """
        Récupère un secteur par son code GICS.
        
        Args:
            db (Session): Session de base de données
            code_gics (str): Code GICS
            
        Returns:
            Optional[Secteur]: Le secteur trouvé ou None
        """
        try:
            secteur = db.query(self.model).filter(self.model.code_gics == code_gics).first()
            if secteur:
                logger.info(f"Secteur trouvé avec le code GICS {code_gics}")
            else:
                logger.warning(f"Aucun secteur trouvé avec le code GICS {code_gics}")
            return secteur
        except Exception as e:
            logger.error(f"Erreur lors de la recherche du secteur par code GICS {code_gics}: {str(e)}")
            raise

class TypeActifCRUD(BaseCRUD[TypeActif]):
    """CRUD pour les types d'actifs."""
    def __init__(self):
        super().__init__(TypeActif)

class SousTypeActifCRUD(BaseCRUD[SousTypeActif]):
    """CRUD pour les sous-types d'actifs."""
    def __init__(self):
        super().__init__(SousTypeActif)
    
    async def get_by_type(self, db: Session, type_id: int) -> List[SousTypeActif]:
        """
        Récupère tous les sous-types d'un type d'actif.
        
        Args:
            db (Session): Session de base de données
            type_id (int): ID du type d'actif
            
        Returns:
            List[SousTypeActif]: Liste des sous-types
        """
        try:
            sous_types = db.query(self.model).filter(self.model.id_type_actif == type_id).all()
            logger.info(f"{len(sous_types)} sous-types trouvés pour le type {type_id}")
            return sous_types
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sous-types du type {type_id}: {str(e)}")
            raise

class ClassifCRUD(BaseCRUD[Classif]):
    """CRUD pour les classifications."""
    def __init__(self):
        super().__init__(Classif)

class SousClassifCRUD(BaseCRUD[SousClassif]):
    """CRUD pour les sous-classifications."""
    def __init__(self):
        super().__init__(SousClassif)
    
    async def get_by_classif(self, db: Session, classif_id: int) -> List[SousClassif]:
        """
        Récupère toutes les sous-classifications d'une classification.
        
        Args:
            db (Session): Session de base de données
            classif_id (int): ID de la classification
            
        Returns:
            List[SousClassif]: Liste des sous-classifications
        """
        try:
            sous_classifs = db.query(self.model).filter(self.model.id_classif == classif_id).all()
            logger.info(f"{len(sous_classifs)} sous-classifications trouvées pour la classification {classif_id}")
            return sous_classifs
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sous-classifications de {classif_id}: {str(e)}")
            raise

class TitreCRUD(BaseCRUD[Titre]):
    """CRUD pour les titres."""
    def __init__(self):
        super().__init__(Titre)
    
    async def get_by_isin(self, db: Session, isin: str) -> Optional[Titre]:
        """
        Récupère un titre par son code ISIN.
        
        Args:
            db (Session): Session de base de données
            isin (str): Code ISIN
            
        Returns:
            Optional[Titre]: Le titre trouvé ou None
        """
        try:
            titre = db.query(self.model).filter(self.model.isin == isin).first()
            if titre:
                logger.info(f"Titre trouvé avec l'ISIN {isin}")
            else:
                logger.warning(f"Aucun titre trouvé avec l'ISIN {isin}")
            return titre
        except Exception as e:
            logger.error(f"Erreur lors de la recherche du titre par ISIN {isin}: {str(e)}")
            raise

class IndiceCRUD(BaseCRUD[Indice]):
    """CRUD pour les indices."""
    def __init__(self):
        super().__init__(Indice)

class FondsCRUD(BaseCRUD[Fonds]):
    """CRUD pour les fonds."""
    def __init__(self):
        super().__init__(Fonds)
    
    async def get_by_gestionnaire(self, db: Session, gestionnaire_id: int) -> List[Fonds]:
        """
        Récupère tous les fonds d'un gestionnaire.
        
        Args:
            db (Session): Session de base de données
            gestionnaire_id (int): ID du gestionnaire
            
        Returns:
            List[Fonds]: Liste des fonds
        """
        try:
            fonds = (
                db.query(self.model)
                .join(self.model.gestionnaires)
                .filter(self.model.gestionnaires.any(id_gestionnaire=gestionnaire_id))
                .all()
            )
            logger.info(f"{len(fonds)} fonds trouvés pour le gestionnaire {gestionnaire_id}")
            return fonds
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des fonds du gestionnaire {gestionnaire_id}: {str(e)}")
            raise

class CompositionFondsCRUD(BaseCRUD[CompositionFonds]):
    """CRUD pour les compositions de fonds."""
    def __init__(self):
        super().__init__(CompositionFonds)
    
    async def get_composition_date(
        self, db: Session, fonds_id: int, date_composition: date
    ) -> List[CompositionFonds]:
        """
        Récupère la composition d'un fonds à une date donnée.
        
        Args:
            db (Session): Session de base de données
            fonds_id (int): ID du fonds
            date_composition (date): Date de la composition
            
        Returns:
            List[CompositionFonds]: Liste des positions
        """
        try:
            positions = (
                db.query(self.model)
                .filter(
                    and_(
                        self.model.id_fonds == fonds_id,
                        self.model.date == date_composition
                    )
                )
                .all()
            )
            logger.info(f"{len(positions)} positions trouvées pour le fonds {fonds_id} au {date_composition}")
            return positions
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la composition du fonds {fonds_id}: {str(e)}")
            raise

class CompositionPortefeuilleCRUD(BaseCRUD[CompositionPortefeuille]):
    """CRUD pour les compositions de portefeuilles."""
    def __init__(self):
        super().__init__(CompositionPortefeuille)
    
    async def get_composition_date(
        self, db: Session, portefeuille_id: int, date_composition: date
    ) -> List[CompositionPortefeuille]:
        """
        Récupère la composition d'un portefeuille à une date donnée.
        
        Args:
            db (Session): Session de base de données
            portefeuille_id (int): ID du portefeuille
            date_composition (date): Date de la composition
            
        Returns:
            List[CompositionPortefeuille]: Liste des positions
        """
        try:
            positions = (
                db.query(self.model)
                .filter(
                    and_(
                        self.model.id_portefeuille == portefeuille_id,
                        self.model.date == date_composition
                    )
                )
                .all()
            )
            logger.info(f"{len(positions)} positions trouvées pour le portefeuille {portefeuille_id} au {date_composition}")
            return positions
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la composition du portefeuille {portefeuille_id}: {str(e)}")
            raise

class CompositionIndiceCRUD(BaseCRUD[CompositionIndice]):
    """CRUD pour les compositions d'indices."""
    def __init__(self):
        super().__init__(CompositionIndice)
    
    async def get_composition_date(
        self, db: Session, indice_id: int, date_composition: date
    ) -> List[CompositionIndice]:
        """
        Récupère la composition d'un indice à une date donnée.
        
        Args:
            db (Session): Session de base de données
            indice_id (int): ID de l'indice
            date_composition (date): Date de la composition
            
        Returns:
            List[CompositionIndice]: Liste des positions
        """
        try:
            positions = (
                db.query(self.model)
                .filter(
                    and_(
                        self.model.id_indice == indice_id,
                        self.model.date == date_composition
                    )
                )
                .all()
            )
            logger.info(f"{len(positions)} positions trouvées pour l'indice {indice_id} au {date_composition}")
            return positions
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la composition de l'indice {indice_id}: {str(e)}")
            raise

# Instances des CRUD
gestionnaire_crud = GestionnaireCRUD()
region_crud = RegionCRUD()
pays_crud = PaysCRUD()
devise_crud = DeviseCRUD()
secteur_crud = SecteurCRUD()
type_actif_crud = TypeActifCRUD()
sous_type_actif_crud = SousTypeActifCRUD()
classif_crud = ClassifCRUD()
sous_classif_crud = SousClassifCRUD()
titre_crud = TitreCRUD()
indice_crud = IndiceCRUD()
fonds_crud = FondsCRUD()
composition_fonds_crud = CompositionFondsCRUD()
composition_portefeuille_crud = CompositionPortefeuilleCRUD()
composition_indice_crud = CompositionIndiceCRUD() 