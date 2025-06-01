"""
Modèles de base pour tous les modèles de données.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class BaseModel(Base):
    """Classe de base pour tous les modèles."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertit le modèle en dictionnaire."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class BaseCodeNom(BaseModel):
    """Classe de base pour les modèles avec code et nom."""
    
    __abstract__ = True
    
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True) 