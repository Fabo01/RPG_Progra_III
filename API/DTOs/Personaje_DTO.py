from pydantic import BaseModel, Field, validator
from typing import Optional

class PersonajeBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)

class PersonajeCreacion(PersonajeBase):
    pass

class PersonajeActualizacion(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)

class PersonajeRespuesta(PersonajeBase):
    id: int
    nivel: int
    experiencia: int
    salud: int
    mana: int
    oro: float
    misiones_completadas: int
    misiones_canceladas: int
    
    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

class PersonajeRanking(BaseModel):
    id: int
    nombre: str
    nivel: int
    misiones_completadas: int
    
    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes
