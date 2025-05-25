from pydantic import BaseModel

class Fonds(BaseModel):
    id: int
    code: str
    nom: str
