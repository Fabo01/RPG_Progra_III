from sqlalchemy.orm import Session
from Repositorios.Mision_Repo import MisionRepositorio
from Repositorios.PersonajeMision_Repo import PersonajeMisionRepositorio
from Servicios.Cola_Serv import ColaServicio
from Utilidades.Excepciones import MisionNoEncontradaError
from datetime import datetime

class MisionServicio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.mision_repo = MisionRepositorio(db_session)
        self.personaje_mision_repo = PersonajeMisionRepositorio(db_session)
        self.cola_servicio = ColaServicio(db_session)
    
    def crear_mision(self, mision_dto):
        """Crea una nueva misión a partir del DTO"""
        # Convertir DTO a dict para crear misión
        mision_data = mision_dto.dict()
        mision_data['fecha_creacion'] = datetime.now()
        mision_data['estado'] = 'pendiente'
        
        return self.mision_repo.crear_mision(mision_data)
    
    def obtener_mision(self, mision_id):
        """Obtiene una misión por su ID"""
        return self.mision_repo.obtener_mision_por_id(mision_id)
    
    def obtener_todas_misiones(self, skip=0, limit=100):
        """Obtiene todas las misiones con paginación"""
        return self.mision_repo.obtener_todas_misiones(skip, limit)
    
    def actualizar_mision(self, mision_id, mision_dto):
        """Actualiza una misión existente"""
        return self.mision_repo.actualizar_mision(mision_id, mision_dto.dict(exclude_unset=True))
    
    def eliminar_mision(self, mision_id):
        """Elimina una misión"""
        return self.mision_repo.eliminar_mision(mision_id)
    
    def obtener_misiones_por_tipo(self, tipo, skip=0, limit=100):
        """Obtiene misiones por tipo"""
        return self.mision_repo.obtener_misiones_por_tipo(tipo, skip, limit)
    
    def obtener_misiones_por_categoria(self, categoria, skip=0, limit=100):
        """Obtiene misiones por categoría"""
        return self.mision_repo.obtener_misiones_por_categoria(categoria, skip, limit)
    
    def obtener_misiones_por_dificultad(self, dificultad_min, dificultad_max, skip=0, limit=100):
        """Obtiene misiones en un rango de dificultad"""
        return self.mision_repo.obtener_misiones_por_dificultad(dificultad_min, dificultad_max, skip, limit)
    
    def asignar_mision_a_personaje(self, mision_id, personaje_id):
        """Asigna una misión a un personaje"""
        # Primero verificar que exista la misión
        mision = self.mision_repo.obtener_mision_por_id(mision_id)
        
        # Crear la relación personaje-misión
        personaje_mision = self.personaje_mision_repo.asignar_mision(personaje_id, mision_id)
        
        # Encolar la misión según su categoría
        es_principal = mision.categoria == 'principal'
        self.cola_servicio.encolar_mision(personaje_id, mision_id, es_principal)
        
        return personaje_mision
    
    def completar_mision_personaje(self, mision_id, personaje_id):
        """Marca como completada una misión para un personaje"""
        # Obtener la misión para verificar su categoría
        mision = self.mision_repo.obtener_mision_por_id(mision_id)
        es_principal = mision.categoria == 'principal'
        
        # Desencolar la misión si está en la cola
        try:
            mision_desencolada = self.cola_servicio.desencolar_mision(personaje_id, es_principal)
            # Verificar que sea la misión que se está completando
            if mision_desencolada and mision_desencolada.mision_id != mision_id:
                # No era la misión esperada, devolver mensaje de error
                raise ValueError(f"La misión {mision_id} no es la primera en la cola {mision.categoria}")
        except:
            # Si hay error al desencolar (por ejemplo, no está en la cola), continuamos
            pass
        
        # Actualizar el estado en la relación
        return self.personaje_mision_repo.actualizar_estado(personaje_id, mision_id, 'completada')
    
    def cancelar_mision_personaje(self, mision_id, personaje_id):
        """Marca como cancelada una misión para un personaje"""
        # Obtener la misión para verificar su categoría
        mision = self.mision_repo.obtener_mision_por_id(mision_id)
        es_principal = mision.categoria == 'principal'
        
        # Intentar desencolar la misión si está en la cola
        try:
            self.cola_servicio.desencolar_mision(personaje_id, es_principal)
        except:
            # Si hay error al desencolar, continuamos
            pass
        
        # Actualizar el estado en la relación
        return self.personaje_mision_repo.actualizar_estado(personaje_id, mision_id, 'cancelada')
    
    def obtener_personajes_por_mision(self, mision_id, estado=None):
        """Obtiene todos los personajes asignados a una misión"""
        relaciones = self.personaje_mision_repo.obtener_personajes_por_mision(mision_id, estado)
        personajes = [relacion.personaje for relacion in relaciones]
        return personajes
    
    def obtener_misiones_por_personaje(self, personaje_id, estado=None):
        """Obtiene todas las misiones asignadas a un personaje"""
        relaciones = self.personaje_mision_repo.obtener_misiones_por_personaje(personaje_id, estado)
        misiones = [relacion.mision for relacion in relaciones]
        return misiones
