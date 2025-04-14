from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

TIPOS_MISION = ['sigilo', 'combate', 'rescate', 'escolta', 'exploracion', 'recoleccion']

class MisionBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=10)
    tipo: str = Field(..., description=f"Tipo de misión: {', '.join(TIPOS_MISION)}")
    categoria: str = Field(..., pattern='^(principal|secundaria)$')
    dificultad: int = Field(..., ge=1, le=10)
    experiencia: float = Field(..., gt=0)
    recompensa_oro: float = Field(..., ge=0)
    
    @validator('tipo')
    def tipo_valido(cls, v):
        if v not in TIPOS_MISION:
            raise ValueError(f'El tipo debe ser uno de: {", ".join(TIPOS_MISION)}')
        return v
    

class MisionCreacion(MisionBase):
    pass

class MisionActualizacion(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=10)
    tipo: Optional[str] = Field(None, min_length=3)
    categoria: Optional[str] = None
    dificultad: Optional[int] = Field(None, ge=1, le=10)
    experiencia: Optional[float] = Field(None, gt=0)
    recompensa_oro: Optional[float] = Field(None, ge=0)
    
    @validator('categoria')
    def categoria_valida(cls, v):
        if v is not None and v not in ['principal', 'secundaria']:
            raise ValueError('La categoría debe ser "principal" o "secundaria"')
        return v

class MisionRespuesta(MisionBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class MisionConPersonajes(MisionRespuesta):
    personajes: List[int] = []
    
    class Config:
        from_attributes = True
