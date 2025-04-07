from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

TIPOS_MISION = ['sigilo', 'combate', 'rescate', 'escolta', 'exploracion', 'recoleccion']

class MisionBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=10)
    tipo: str = Field(..., description=f"Tipo de misión: {', '.join(TIPOS_MISION)}")
    categoria: str = Field(..., pattern='^(principal|secundaria)$')  # Cambiado de regex a pattern
    dificultad: int = Field(..., ge=1, le=10)
    experiencia: float = Field(..., gt=0)
    recompensa_oro: float = Field(..., ge=0)
    
    @validator('tipo')
    def tipo_valido(cls, v):
        if v not in TIPOS_MISION:
            raise ValueError(f'El tipo debe ser uno de: {", ".join(TIPOS_MISION)}')
        return v
    
    @validator('categoria')
    def categoria_valida(cls, v):
        if v not in ['principal', 'secundaria']:
            raise ValueError('La categoría debe ser "principal" o "secundaria"')
        return v

class MisionCreacion(MisionBase):
    fecha_limite: Optional[datetime] = None

class MisionActualizacion(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=10)
    tipo: Optional[str] = Field(None, min_length=3)
    categoria: Optional[str] = None
    dificultad: Optional[int] = Field(None, ge=1, le=10)
    experiencia: Optional[float] = Field(None, gt=0)
    recompensa_oro: Optional[float] = Field(None, ge=0)
    estado: Optional[str] = None
    fecha_limite: Optional[datetime] = None
    
    @validator('categoria')
    def categoria_valida(cls, v):
        if v is not None and v not in ['principal', 'secundaria']:
            raise ValueError('La categoría debe ser "principal" o "secundaria"')
        return v
        
    @validator('estado')
    def estado_valido(cls, v):
        if v is not None and v not in ['pendiente', 'completada', 'cancelada']:
            raise ValueError('El estado debe ser "pendiente", "completada" o "cancelada"')
        return v

class MisionRespuesta(MisionBase):
    id: int
    estado: str
    fecha_creacion: datetime
    fecha_limite: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes

class MisionConPersonajes(MisionRespuesta):
    personajes: List[int] = []  # Lista de IDs de personajes asignados
    
    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes
