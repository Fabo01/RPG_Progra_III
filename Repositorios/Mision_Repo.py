from sqlalchemy.orm import Session
from sqlalchemy import desc
from Modelos.Mision import Mision
from datetime import datetime
from Utilidades.Excepciones import MisionNoEncontradaError

class MisionRepositorio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def crear_mision(self, mision_data):
        """Crea una nueva misión en la base de datos"""
        # Asegurar que tenga fecha de creación
        if 'fecha_creacion' not in mision_data:
            mision_data['fecha_creacion'] = datetime.now()
            
        nueva_mision = Mision(**mision_data)
        self.db_session.add(nueva_mision)
        self.db_session.commit()
        self.db_session.refresh(nueva_mision)
        return nueva_mision
    
    def obtener_mision_por_id(self, mision_id):
        """Obtiene una misión por su ID"""
        mision = self.db_session.query(Mision).filter(Mision.id == mision_id).first()
        if not mision:
            raise MisionNoEncontradaError(f"No se encontró la misión con ID {mision_id}")
        return mision
    
    def obtener_todas_misiones(self, skip=0, limit=100):
        """Obtiene todas las misiones con paginación opcional"""
        return self.db_session.query(Mision).offset(skip).limit(limit).all()
    
    def obtener_misiones_por_tipo(self, tipo, skip=0, limit=100):
        """Obtiene misiones por tipo (exploración, combate, etc)"""
        return self.db_session.query(Mision).filter(
            Mision.tipo == tipo
        ).offset(skip).limit(limit).all()
    
    def obtener_misiones_por_categoria(self, categoria, skip=0, limit=100):
        """Obtiene misiones por categoría (principal, secundaria)"""
        return self.db_session.query(Mision).filter(
            Mision.categoria == categoria
        ).offset(skip).limit(limit).all()
    
    def obtener_misiones_por_dificultad(self, dificultad_min, dificultad_max, skip=0, limit=100):
        """Obtiene misiones en un rango de dificultad"""
        return self.db_session.query(Mision).filter(
            Mision.dificultad >= dificultad_min,
            Mision.dificultad <= dificultad_max
        ).offset(skip).limit(limit).all()
    
    def actualizar_mision(self, mision_id, mision_data):
        """Actualiza una misión existente"""
        mision = self.obtener_mision_por_id(mision_id)
        for key, value in mision_data.items():
            setattr(mision, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(mision)
        return mision
    
    def eliminar_mision(self, mision_id):
        """Elimina una misión de la base de datos"""
        mision = self.obtener_mision_por_id(mision_id)
        self.db_session.delete(mision)
        self.db_session.commit()
        return {"mensaje": f"Misión {mision_id} eliminada"}
