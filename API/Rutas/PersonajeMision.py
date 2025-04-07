from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from Config.db import get_db
from API.DTOs.Mision_DTO import MisionRespuesta
from API.DTOs.Personaje_DTO import PersonajeRespuesta
from Servicios.Mision_Serv import MisionServicio
from Servicios.Personaje_Serv import PersonajeServicio
from Servicios.Cola_Serv import ColaServicio
from Utilidades.Excepciones import MisionNoEncontradaError, PersonajeNoEncontradoError

router = APIRouter(
    prefix="/personajes-misiones",
    tags=["personajes-misiones"]
)

# Asignación de misiones (centralizamos aquí todos los endpoints relacionados)
@router.post("/asignar/{mision_id}/a/{personaje_id}")
def asignar_mision(mision_id: int, personaje_id: int, db: Session = Depends(get_db)):
    """
    Asigna una misión a un personaje y la encola según su categoría
    """
    servicio = MisionServicio(db)
    try:
        return servicio.asignar_mision_a_personaje(mision_id, personaje_id)
    except (MisionNoEncontradaError, PersonajeNoEncontradoError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/completar/{mision_id}/personaje/{personaje_id}")
def completar_mision(mision_id: int, personaje_id: int, db: Session = Depends(get_db)):
    """
    Marca una misión como completada para un personaje, la desencola y otorga recompensas
    """
    servicio = MisionServicio(db)
    try:
        # Primero actualizar estado
        mision_actualizada = servicio.completar_mision_personaje(mision_id, personaje_id)
        # Luego calcular y otorgar recompensas
        servicio_personaje = PersonajeServicio(db)
        resultado_recompensa = servicio_personaje.otorgar_recompensas_mision(personaje_id, mision_id)
        return resultado_recompensa
    except (MisionNoEncontradaError, PersonajeNoEncontradoError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancelar/{mision_id}/personaje/{personaje_id}")
def cancelar_mision(mision_id: int, personaje_id: int, db: Session = Depends(get_db)):
    """
    Marca una misión como cancelada para un personaje y la desencola
    """
    servicio = MisionServicio(db)
    personaje_servicio = PersonajeServicio(db)
    try:
        # Cancelar en la tabla de relación y desencolar
        servicio.cancelar_mision_personaje(mision_id, personaje_id)
        # Incrementar el contador de misiones canceladas
        return personaje_servicio.registrar_mision_cancelada(personaje_id, mision_id)
    except (MisionNoEncontradaError, PersonajeNoEncontradoError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/personaje/{personaje_id}/cola/{tipo_cola}")
def obtener_cola_misiones(personaje_id: int, tipo_cola: str, db: Session = Depends(get_db)):
    """
    Obtiene la cola de misiones de un personaje (principal o secundaria)
    """
    if tipo_cola not in ['principal', 'secundaria']:
        raise HTTPException(status_code=400, detail="El tipo de cola debe ser 'principal' o 'secundaria'")
    
    servicio = ColaServicio(db)
    try:
        es_principal = tipo_cola == 'principal'
        # Obtener información de la cola
        cola_vacia = servicio.esta_vacia_cola(personaje_id, es_principal)
        tamano = servicio.obtener_tamano_cola(personaje_id, es_principal)
        proxima = servicio.obtener_primera_mision(personaje_id, es_principal)
        
        # Preparar respuesta
        return {
            "personaje_id": personaje_id,
            "tipo_cola": tipo_cola,
            "esta_vacia": cola_vacia,
            "tamano": tamano,
            "proxima_mision": proxima.mision if proxima else None
        }
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/personaje/{personaje_id}/misiones", response_model=List[MisionRespuesta])
def obtener_misiones_por_personaje(
    personaje_id: int, 
    estado: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las misiones asignadas a un personaje
    """
    servicio = MisionServicio(db)
    try:
        return servicio.obtener_misiones_por_personaje(personaje_id, estado)
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/mision/{mision_id}/personajes", response_model=List[PersonajeRespuesta])
def obtener_personajes_por_mision(
    mision_id: int, 
    estado: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los personajes asignados a una misión
    """
    servicio = MisionServicio(db)
    try:
        return servicio.obtener_personajes_por_mision(mision_id, estado)
    except MisionNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))
