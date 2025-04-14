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
    
    def desencolar_mision_especifica(self, personaje_id: int, mision_id: int, es_principal: bool = False):
        """
        Elimina una misión específica de la cola del personaje, independiente de su posición.
        Útil para eliminar asignaciones de misiones cuando se quiere eliminar la misión.
        
        Args:
            personaje_id: ID del personaje dueño de la cola
            mision_id: ID de la misión a eliminar de la cola
            es_principal: True si se trata de la cola principal, False si es la secundaria
            
        Returns:
            La relación PersonajesMisiones que fue eliminada o None si no se encontró
            
        Raises:
            ColaVaciaError: Si la cola está vacía
            MisionNoEncontradaError: Si la misión no se encuentra en la cola
        """
        tipo_cola = 'principal' if es_principal else 'secundaria'
        
        # Obtenemos la cola
        cola_tda = self.obtener_cola_personaje(personaje_id, tipo_cola)
        
        # Verificamos si la cola está vacía
        if cola_tda.is_empty():
            raise ColaVaciaError(f"La cola {tipo_cola} del personaje {personaje_id} está vacía")
        
        # Creamos una nueva cola para guardar las misiones que no vamos a eliminar
        nueva_cola = TDA_Cola()
        mision_eliminada = None
        
        # Iteramos por las misiones para encontrar la que queremos eliminar
        for _ in range(cola_tda.size()):
            mision = cola_tda.dequeue()
            if mision.mision_id == mision_id:
                mision_eliminada = mision
            else:
                nueva_cola.enqueue(mision)
        
        # Si no encontramos la misión, lanzamos una excepción
        if not mision_eliminada:
            # Restauramos la cola original
            while not nueva_cola.is_empty():
                cola_tda.enqueue(nueva_cola.dequeue())
            raise MisionNoEncontradaError(f"La misión {mision_id} no está en la cola {tipo_cola} del personaje {personaje_id}")
        
        # Guardamos la nueva cola actualizada (sin la misión eliminada)
        self.guardar_cola_personaje(personaje_id, tipo_cola, nueva_cola)
        
        return mision_eliminada
    
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
