from sqlalchemy.orm import Session
from Modelos.PersonajesMisiones import PersonajesMisiones
from Modelos.Personaje import Personaje
from Modelos.Mision import Mision
from datetime import datetime

class PersonajeMisionRepositorio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def asignar_mision(self, personaje_id, mision_id):
        """Asigna una misión a un personaje"""
        # Verificar que no exista ya la asignación
        relacion = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id, 
            mision_id=mision_id
        ).first()
        
        if relacion:
            return relacion  # La misión ya está asignada
        
        # Crear nueva asignación
        nueva_asignacion = PersonajesMisiones(
            personaje_id=personaje_id,
            mision_id=mision_id,
            estado='pendiente',
            fecha_asignacion=datetime.now()
        )
        
        self.db_session.add(nueva_asignacion)
        self.db_session.commit()
        self.db_session.refresh(nueva_asignacion)
        return nueva_asignacion
    
    def actualizar_estado(self, personaje_id, mision_id, nuevo_estado):
        """Actualiza el estado de una misión para un personaje"""
        relacion = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id, 
            mision_id=mision_id
        ).first()
        
        if not relacion:
            raise ValueError(f"La misión {mision_id} no está asignada al personaje {personaje_id}")
        
        relacion.estado = nuevo_estado
        
        # Si está completando o cancelando, registrar fecha
        if nuevo_estado in ['completada', 'cancelada']:
            relacion.fecha_finalizacion = datetime.now()
        
        self.db_session.commit()
        self.db_session.refresh(relacion)
        return relacion
    
    def obtener_misiones_por_personaje(self, personaje_id, estado=None):
        """Obtiene todas las misiones de un personaje, opcionalmente filtradas por estado"""
        query = self.db_session.query(PersonajesMisiones).filter(
            PersonajesMisiones.personaje_id == personaje_id
        )
        
        if estado:
            query = query.filter(PersonajesMisiones.estado == estado)
            
        return query.all()
    
    def obtener_personajes_por_mision(self, mision_id, estado=None):
        """Obtiene todos los personajes asignados a una misión, opcionalmente filtrados por estado"""
        query = self.db_session.query(PersonajesMisiones).filter(
            PersonajesMisiones.mision_id == mision_id
        )
        
        if estado:
            query = query.filter(PersonajesMisiones.estado == estado)
            
        return query.all()
    
    def eliminar_asignacion(self, personaje_id, mision_id):
        """Elimina la asignación de una misión a un personaje"""
        relacion = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id, 
            mision_id=mision_id
        ).first()
        
        if not relacion:
            return {"mensaje": "La asignación no existe"}
        
        self.db_session.delete(relacion)
        self.db_session.commit()
        return {"mensaje": f"Asignación de misión {mision_id} a personaje {personaje_id} eliminada"}
