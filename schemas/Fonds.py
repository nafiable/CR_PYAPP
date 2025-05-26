from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Fonds(BaseModel):
    id: int
    code: str
    nom: str
