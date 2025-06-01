"""
Module de base pour les opérations CRUD.
"""

import logging
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from schemas.base import BaseModel

logger = logging.getLogger(__name__)

# Type générique pour les modèles
ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseCRUD(Generic[ModelType]):
    """
    Classe de base pour les opérations CRUD.
    
    Cette classe fournit les opérations de base Create, Read, Update, Delete
    pour n'importe quel modèle SQLAlchemy.
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialise le CRUD avec un modèle SQLAlchemy.
        
        Args:
            model (Type[ModelType]): Classe du modèle SQLAlchemy
        """
        self.model = model
    
    async def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """
        Crée un nouvel objet dans la base de données.
        
        Args:
            db (Session): Session de base de données
            obj_in (Dict[str, Any]): Données de l'objet à créer
            
        Returns:
            ModelType: L'objet créé
        """
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Objet {self.model.__name__} créé avec succès")
            return db_obj
        except Exception as e:
            db.rollback()
            logger.error(f"Erreur lors de la création de {self.model.__name__}: {str(e)}")
            raise
    
    async def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Récupère un objet par son ID.
        
        Args:
            db (Session): Session de base de données
            id (int): ID de l'objet
            
        Returns:
            Optional[ModelType]: L'objet trouvé ou None
        """
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
            if obj:
                logger.info(f"{self.model.__name__} {id} trouvé")
            else:
                logger.warning(f"{self.model.__name__} {id} non trouvé")
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de {self.model.__name__} {id}: {str(e)}")
            raise
    
    async def get_by_code(self, db: Session, code: str) -> Optional[ModelType]:
        """
        Récupère un objet par son code.
        
        Args:
            db (Session): Session de base de données
            code (str): Code de l'objet
            
        Returns:
            Optional[ModelType]: L'objet trouvé ou None
        """
        try:
            obj = db.query(self.model).filter(self.model.code == code).first()
            if obj:
                logger.info(f"{self.model.__name__} avec code {code} trouvé")
            else:
                logger.warning(f"{self.model.__name__} avec code {code} non trouvé")
            return obj
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de {self.model.__name__} avec code {code}: {str(e)}")
            raise
    
    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Récupère plusieurs objets avec pagination.
        
        Args:
            db (Session): Session de base de données
            skip (int): Nombre d'objets à sauter
            limit (int): Nombre maximum d'objets à retourner
            
        Returns:
            List[ModelType]: Liste des objets
        """
        try:
            objs = db.query(self.model).offset(skip).limit(limit).all()
            logger.info(f"{len(objs)} {self.model.__name__}(s) récupéré(s)")
            return objs
        except Exception as e:
            logger.error(f"Erreur lors de la récupération multiple de {self.model.__name__}: {str(e)}")
            raise
    
    async def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[Dict[str, Any], ModelType]
    ) -> ModelType:
        """
        Met à jour un objet.
        
        Args:
            db (Session): Session de base de données
            db_obj (ModelType): Objet existant
            obj_in (Union[Dict[str, Any], ModelType]): Données de mise à jour
            
        Returns:
            ModelType: L'objet mis à jour
        """
        try:
            obj_data = db_obj.to_dict()
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.to_dict()
                
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            
            logger.info(f"{self.model.__name__} {db_obj.id} mis à jour")
            return db_obj
        except Exception as e:
            db.rollback()
            logger.error(f"Erreur lors de la mise à jour de {self.model.__name__} {db_obj.id}: {str(e)}")
            raise
    
    async def delete(self, db: Session, *, id: int) -> ModelType:
        """
        Supprime un objet.
        
        Args:
            db (Session): Session de base de données
            id (int): ID de l'objet à supprimer
            
        Returns:
            ModelType: L'objet supprimé
        """
        try:
            obj = db.query(self.model).get(id)
            if not obj:
                raise ValueError(f"{self.model.__name__} {id} non trouvé")
            
            db.delete(obj)
            db.commit()
            
            logger.info(f"{self.model.__name__} {id} supprimé")
            return obj
        except Exception as e:
            db.rollback()
            logger.error(f"Erreur lors de la suppression de {self.model.__name__} {id}: {str(e)}")
            raise
    
    async def exists(self, db: Session, id: int) -> bool:
        """
        Vérifie si un objet existe.
        
        Args:
            db (Session): Session de base de données
            id (int): ID de l'objet
            
        Returns:
            bool: True si l'objet existe, False sinon
        """
        try:
            exists = db.query(self.model).filter(self.model.id == id).first() is not None
            logger.debug(f"{self.model.__name__} {id} existe: {exists}")
            return exists
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de l'existence de {self.model.__name__} {id}: {str(e)}")
            raise
    
    async def count(self, db: Session) -> int:
        """
        Compte le nombre total d'objets.
        
        Args:
            db (Session): Session de base de données
            
        Returns:
            int: Nombre total d'objets
        """
        try:
            count = db.query(self.model).count()
            logger.debug(f"Nombre total de {self.model.__name__}: {count}")
            return count
        except Exception as e:
            logger.error(f"Erreur lors du comptage de {self.model.__name__}: {str(e)}")
            raise 