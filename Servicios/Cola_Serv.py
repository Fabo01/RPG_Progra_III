from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
from Modelos.ColaFIFO import ColaFIFO
from Modelos.PersonajesMisiones import PersonajesMisiones
from Estructuras.TDA_Cola import TDA_Cola
from Utilidades.Excepciones import ColaVaciaError, MisionNoEncontradaError

class ColaServicio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def obtener_cola_personaje(self, personaje_id: int, tipo_cola: str) -> TDA_Cola:
        """
        Obtiene la cola de misiones de un personaje (principal o secundaria)
        y la convierte a un objeto TDA_Cola para su manipulación.
        """
        cola_db = self.db_session.query(ColaFIFO).filter_by(
            personaje_id=personaje_id, 
            tipo_cola=tipo_cola
        ).first()
        
        # Si no existe la cola, la creamos
        if not cola_db:
            cola_db = ColaFIFO(
                personaje_id=personaje_id,
                tipo_cola=tipo_cola,
                misiones_orden=[]
            )
            self.db_session.add(cola_db)
            self.db_session.commit()
        
        # Convertimos la cola de la BD a un objeto TDA_Cola
        cola_tda = TDA_Cola()
        
        # Si hay misiones en la cola, las obtenemos y las añadimos al TDA_Cola
        if cola_db.misiones_orden:
            misiones_ids = cola_db.misiones_orden
            misiones = self.db_session.query(PersonajesMisiones).filter(
                PersonajesMisiones.personaje_id == personaje_id,
                PersonajesMisiones.mision_id.in_(misiones_ids)
            ).all()
            
            # Ordenamos las misiones según el orden en la cola
            for mision_id in misiones_ids:
                for mision in misiones:
                    if mision.mision_id == mision_id:
                        cola_tda.enqueue(mision)
                        break
        
        return cola_tda
    
    def guardar_cola_personaje(self, personaje_id: int, tipo_cola: str, cola_tda: TDA_Cola):
        """
        Guarda el estado actual de la cola TDA en la base de datos.
        """
        cola_db = self.db_session.query(ColaFIFO).filter_by(
            personaje_id=personaje_id, 
            tipo_cola=tipo_cola
        ).first()
        
        if not cola_db:
            cola_db = ColaFIFO(
                personaje_id=personaje_id,
                tipo_cola=tipo_cola
            )
            self.db_session.add(cola_db)
        
        # Convertir la cola TDA a una lista de IDs de misiones
        misiones_ids = []
        for item in cola_tda.items:
            misiones_ids.append(item.mision_id)
        
        cola_db.misiones_orden = misiones_ids
        self.db_session.commit()
    
    def encolar_mision(self, personaje_id: int, mision_id: int, es_principal: bool = False):
        """
        Añade una misión a la cola correspondiente del personaje.
        """
        # Verificamos que exista la relación personaje-misión
        personaje_mision = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id,
            mision_id=mision_id
        ).first()
        
        if not personaje_mision:
            raise MisionNoEncontradaError(f"La misión {mision_id} no está asignada al personaje {personaje_id}")
        
        tipo_cola = 'principal' if es_principal else 'secundaria'
        
        # Obtenemos la cola
        cola_tda = self.obtener_cola_personaje(personaje_id, tipo_cola)
        
        # Añadimos la misión a la cola
        cola_tda.enqueue(personaje_mision)
        
        # Guardamos la cola actualizada
        self.guardar_cola_personaje(personaje_id, tipo_cola, cola_tda)
        
        return personaje_mision
    
    def desencolar_mision(self, personaje_id: int, es_principal: bool = False):
        """
        Elimina y retorna la primera misión de la cola del personaje.
        """
        tipo_cola = 'principal' if es_principal else 'secundaria'
        
        # Obtenemos la cola
        cola_tda = self.obtener_cola_personaje(personaje_id, tipo_cola)
        
        # Verificamos si la cola está vacía
        if cola_tda.is_empty():
            raise ColaVaciaError(f"La cola {tipo_cola} del personaje {personaje_id} está vacía")
        
        # Desencolamos la misión
        personaje_mision = cola_tda.dequeue()
        
        # Guardamos la cola actualizada
        self.guardar_cola_personaje(personaje_id, tipo_cola, cola_tda)
        
        return personaje_mision
    
    def obtener_primera_mision(self, personaje_id: int, es_principal: bool = False):
        """
        Retorna la primera misión de la cola sin eliminarla.
        """
        tipo_cola = 'principal' if es_principal else 'secundaria'
        
        # Obtenemos la cola
        cola_tda = self.obtener_cola_personaje(personaje_id, tipo_cola)
        
        # Verificamos si la cola está vacía
        if cola_tda.is_empty():
            return None
        
        return cola_tda.first()
    
    def esta_vacia_cola(self, personaje_id: int, es_principal: bool = False):
        """
        Verifica si la cola está vacía.
        """
        tipo_cola = 'principal' if es_principal else 'secundaria'
        
        # Obtenemos la cola
        cola_tda = self.obtener_cola_personaje(personaje_id, tipo_cola)
        
        return cola_tda.is_empty()
    
    def obtener_tamano_cola(self, personaje_id: int, es_principal: bool = False):
        """
        Retorna la cantidad de misiones en la cola.
        """
        tipo_cola = 'principal' if es_principal else 'secundaria'
        
        # Obtenemos la cola
        cola_tda = self.obtener_cola_personaje(personaje_id, tipo_cola)
        
        return cola_tda.size()
