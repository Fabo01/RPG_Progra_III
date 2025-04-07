from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from Config.db import get_db
from API.DTOs.Mision_DTO import MisionCreacion, MisionRespuesta, MisionActualizacion, MisionConPersonajes
from API.DTOs.Personaje_DTO import PersonajeRespuesta
from Servicios.Mision_Serv import MisionServicio
from Utilidades.Excepciones import MisionNoEncontradaError

router = APIRouter(
    prefix="/misiones",
    tags=["misiones"]
)

@router.post("/", response_model=MisionRespuesta, status_code=status.HTTP_201_CREATED)
def crear_mision(mision: MisionCreacion, db: Session = Depends(get_db)):
    """
    Crea una nueva misión en el sistema
    """
    servicio = MisionServicio(db)
    return servicio.crear_mision(mision)

@router.get("/", response_model=List[MisionRespuesta])
def obtener_misiones(
    tipo: Optional[str] = None,
    categoria: Optional[str] = None,
    dificultad_min: Optional[int] = None,
    dificultad_max: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de misiones con filtros opcionales
    """
    servicio = MisionServicio(db)
    
    # Aplicar filtros según los parámetros proporcionados
    if tipo:
        return servicio.obtener_misiones_por_tipo(tipo, skip, limit)
    elif categoria:
        return servicio.obtener_misiones_por_categoria(categoria, skip, limit)
    elif dificultad_min and dificultad_max:
        return servicio.obtener_misiones_por_dificultad(dificultad_min, dificultad_max, skip, limit)
    else:
        return servicio.obtener_todas_misiones(skip, limit)

@router.get("/{mision_id}", response_model=MisionRespuesta)
def obtener_mision(mision_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una misión por su ID
    """
    servicio = MisionServicio(db)
    try:
        return servicio.obtener_mision(mision_id)
    except MisionNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{mision_id}/personajes", response_model=List[PersonajeRespuesta])
def obtener_personajes_de_mision(
    mision_id: int, 
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los personajes asignados a una misión, con filtro opcional por estado
    """
    servicio = MisionServicio(db)
    try:
        return servicio.obtener_personajes_por_mision(mision_id, estado)
    except MisionNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{mision_id}", response_model=MisionRespuesta)
def actualizar_mision(mision_id: int, mision: MisionActualizacion, db: Session = Depends(get_db)):
    """
    Actualiza una misión existente
    """
    servicio = MisionServicio(db)
    try:
        return servicio.actualizar_mision(mision_id, mision)
    except MisionNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{mision_id}")
def eliminar_mision(mision_id: int, db: Session = Depends(get_db)):
    """
    Elimina una misión del sistema
    """
    servicio = MisionServicio(db)
    try:
        return servicio.eliminar_mision(mision_id)
    except MisionNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
