from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Config.db import get_db
from API.DTOs.Personaje_DTO import (
    PersonajeCreacion, 
    PersonajeRespuesta, 
    PersonajeActualizacion,
    PersonajeRanking
)
from API.DTOs.Mision_DTO import MisionRespuesta
from Servicios.Personaje_Serv import PersonajeServicio
from Servicios.Mision_Serv import MisionServicio
from Utilidades.Excepciones import PersonajeNoEncontradoError, MisionNoEncontradaError, ColaVaciaError

router = APIRouter(
    prefix="/personajes",
    tags=["personajes"]
)

@router.post("/", response_model=PersonajeRespuesta, status_code=status.HTTP_201_CREATED)
def crear_personaje(personaje: PersonajeCreacion, db: Session = Depends(get_db)):
    """
    Crea un nuevo personaje en el sistema
    """
    servicio = PersonajeServicio(db)
    return servicio.crear_personaje(personaje)

@router.get("/", response_model=List[PersonajeRespuesta])
def obtener_personajes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de personajes con paginación
    """
    servicio = PersonajeServicio(db)
    return servicio.obtener_todos_personajes(skip, limit)

@router.get("/ranking", response_model=List[PersonajeRanking])
def obtener_ranking(limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtiene el ranking de personajes por nivel
    """
    servicio = PersonajeServicio(db)
    return servicio.obtener_ranking(limit)

@router.get("/{personaje_id}", response_model=PersonajeRespuesta)
def obtener_personaje(personaje_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un personaje por su ID
    """
    servicio = PersonajeServicio(db)
    try:
        return servicio.obtener_personaje(personaje_id)
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{personaje_id}", response_model=PersonajeRespuesta)
def actualizar_personaje(personaje_id: int, personaje: PersonajeActualizacion, db: Session = Depends(get_db)):
    """
    Actualiza un personaje existente
    """
    servicio = PersonajeServicio(db)
    try:
        return servicio.actualizar_personaje(personaje_id, personaje)
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{personaje_id}")
def eliminar_personaje(personaje_id: int, db: Session = Depends(get_db)):
    """
    Elimina un personaje del sistema
    """
    servicio = PersonajeServicio(db)
    try:
        return servicio.eliminar_personaje(personaje_id)
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{personaje_id}/completar")
def completar_primera_mision(personaje_id: int, tipo_cola: str = None, db: Session = Depends(get_db)):
    """
    Completa la primera misión en la cola especificada del personaje.
    Si no se especifica tipo_cola, se intenta primero con la cola principal y luego con la secundaria.
    
    - tipo_cola: "principal" o "secundaria"
    """
    # Servicios necesarios
    personaje_servicio = PersonajeServicio(db)
    mision_servicio = MisionServicio(db)
    
    try:
        # Importamos el servicio de cola
        from Servicios.Cola_Serv import ColaServicio
        cola_servicio = ColaServicio(db)
        
        # Verificar tipo de cola especificado
        if tipo_cola and tipo_cola not in ["principal", "secundaria"]:
            raise HTTPException(
                status_code=400, 
                detail="El tipo de cola debe ser 'principal' o 'secundaria'"
            )
        
        # Si se especifica el tipo de cola, usamos esa
        if tipo_cola:
            es_principal = tipo_cola == "principal"
            primera_mision = cola_servicio.obtener_primera_mision(personaje_id, es_principal)
            
            if not primera_mision:
                raise HTTPException(
                    status_code=404, 
                    detail=f"El personaje no tiene misiones pendientes en la cola {tipo_cola}"
                )
        else:
            # Comportamiento anterior: intentar primero con la cola principal
            cola_tipo = "principal"
            primera_mision = cola_servicio.obtener_primera_mision(personaje_id, es_principal=True)
            if not primera_mision:
                # Si no hay misiones principales, intentar con la secundaria
                cola_tipo = "secundaria"
                primera_mision = cola_servicio.obtener_primera_mision(personaje_id, es_principal=False)
                
            if not primera_mision:
                raise HTTPException(status_code=404, detail="El personaje no tiene misiones pendientes en ninguna cola")
            
            tipo_cola = cola_tipo
        
        # Obtener el ID de la misión y si es principal
        mision_id = primera_mision.mision_id
        es_principal = tipo_cola == "principal"
        
        try:
            # Completar la misión
            mision_desencolada = cola_servicio.desencolar_mision(personaje_id, es_principal)
            
            # Actualizar estado y dar recompensas
            mision_servicio.personaje_mision_repo.actualizar_estado(personaje_id, mision_id, 'completada')
            resultado = personaje_servicio.otorgar_recompensas_mision(personaje_id, mision_id)
            
            return {
                "mensaje": f"Misión {mision_id} completada con éxito de la cola {tipo_cola}",
                "recompensas": resultado
            }
            
        except ColaVaciaError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al completar la misión: {str(e)}")
        
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{personaje_id}/misiones", response_model=List[MisionRespuesta])
def obtener_misiones_personaje_fifo(personaje_id: int, db: Session = Depends(get_db)):
    """
    Obtiene las misiones del personaje en orden FIFO
    """
    try:
        # Importamos aquí para evitar dependencias circulares
        from Servicios.Cola_Serv import ColaServicio
        cola_servicio = ColaServicio(db)
        
        # Obtener ambas colas
        cola_principal = cola_servicio.obtener_cola_personaje(personaje_id, "principal")
        cola_secundaria = cola_servicio.obtener_cola_personaje(personaje_id, "secundaria")
        
        # Extraer misiones en orden FIFO
        misiones_principales = [item.mision for item in cola_principal.items] if cola_principal else []
        misiones_secundarias = [item.mision for item in cola_secundaria.items] if cola_secundaria else []
        
        # Devolver primero las principales y luego las secundarias (respetando el orden FIFO en cada cola)
        return misiones_principales + misiones_secundarias
        
    except PersonajeNoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

