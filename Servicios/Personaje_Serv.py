from sqlalchemy.orm import Session
from Repositorios.Personaje_Repo import PersonajeRepositorio
from Modelos.PersonajesMisiones import PersonajesMisiones
from datetime import datetime
from Utilidades.Excepciones import PersonajeNoEncontradoError

# Multiplicadores de recompensas según el tipo de misión
MULTIPLICADORES_TIPO_MISION = {
    'sigilo': 1.5,
    'combate': 1.5,
    'rescate': 1.3,
    'escolta': 1.2,
    'exploracion': 1.1,
    'recoleccion': 1.0
}

class PersonajeServicio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.personaje_repo = PersonajeRepositorio(db_session)
    
    def crear_personaje(self, personaje_dto):
        """
        Crea un nuevo personaje a partir del DTO
        """
        # Convertir DTO a dict para crear personaje
        personaje_data = {
            'nombre': personaje_dto.nombre,
            # Valores iniciales por defecto
            'nivel': 1,
            'experiencia': 0,
            'salud': 100,
            'mana': 100,
            'oro': 0.0,
            'misiones_completadas': 0,
            'misiones_canceladas': 0
        }
        
        return self.personaje_repo.crear_personaje(personaje_data)
    
    def obtener_personaje(self, personaje_id):
        """Obtiene un personaje por su ID"""
        return self.personaje_repo.obtener_personaje_por_id(personaje_id)
    
    def obtener_todos_personajes(self, skip=0, limit=100):
        """Obtiene todos los personajes con paginación"""
        return self.personaje_repo.obtener_todos_personajes(skip, limit)
    
    def actualizar_personaje(self, personaje_id, personaje_dto):
        """Actualiza un personaje existente"""
        return self.personaje_repo.actualizar_personaje(personaje_id, personaje_dto.dict(exclude_unset=True))
    
    def eliminar_personaje(self, personaje_id):
        """Elimina un personaje"""
        return self.personaje_repo.eliminar_personaje(personaje_id)
    
    def asignar_mision(self, personaje_id, mision_id):
        """Asigna una misión a un personaje"""
        # Verificar que existe el personaje
        personaje = self.personaje_repo.obtener_personaje_por_id(personaje_id)
        
        # Crear relación personaje-misión
        personaje_mision = PersonajesMisiones(
            personaje_id=personaje_id,
            mision_id=mision_id,
            estado='pendiente',
            fecha_asignacion=datetime.now()
        )
        
        self.db_session.add(personaje_mision)
        self.db_session.commit()
        
        return personaje_mision
    
    def otorgar_recompensas_mision(self, personaje_id, mision_id):
        """Otorga recompensas por completar una misión teniendo en cuenta el tipo de misión"""
        # Obtener relación personaje-misión
        personaje_mision = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id,
            mision_id=mision_id
        ).first()
        
        if not personaje_mision or personaje_mision.estado != 'completada':
            raise ValueError(f"La misión {mision_id} no está completada por el personaje {personaje_id}")
        
        # Obtener personaje y misión
        personaje = self.personaje_repo.obtener_personaje_por_id(personaje_id)
        mision = personaje_mision.mision
        
        # Obtener multiplicador por tipo de misión
        multiplicador_tipo = MULTIPLICADORES_TIPO_MISION.get(mision.tipo, 1.0)
        
        # Calcular recompensas con multiplicador por tipo y dificultad
        exp_ganada = mision.experiencia * (1 + mision.dificultad * 0.1) * multiplicador_tipo
        oro_ganado = mision.recompensa_oro * (1 + mision.dificultad * 0.1) * multiplicador_tipo
        
        # Otorgar recompensas
        personaje.ganar_experiencia(exp_ganada)
        personaje.ganar_oro(oro_ganado)
        personaje.misiones_completadas += 1
        
        self.db_session.commit()
        
        return {
            "personaje": personaje,
            "mision": mision,
            "tipo_mision": mision.tipo,
            "multiplicador_tipo": multiplicador_tipo,
            "experiencia_base": mision.experiencia,
            "experiencia_ganada": exp_ganada,
            "oro_base": mision.recompensa_oro,
            "oro_ganado": oro_ganado,
            "nivel_actual": personaje.nivel
        }
    
    def registrar_mision_cancelada(self, personaje_id, mision_id):
        """Incrementa el contador de misiones canceladas del personaje"""
        personaje = self.personaje_repo.obtener_personaje_por_id(personaje_id)
        personaje.misiones_canceladas += 1
        self.db_session.commit()
        
        return {
            "mensaje": f"Misión {mision_id} cancelada para el personaje {personaje_id}",
            "personaje": personaje
        }
    
    def completar_mision(self, personaje_id, mision_id):
        """Completa una misión y otorga recompensas"""
        # Buscar la relación personaje-misión
        personaje_mision = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id,
            mision_id=mision_id
        ).first()
        
        if not personaje_mision:
            raise ValueError(f"La misión {mision_id} no está asignada al personaje {personaje_id}")
        
        # Actualizar estado de la misión
        personaje_mision.estado = 'completada'
        personaje_mision.fecha_finalizacion = datetime.now()
        self.db_session.commit()
        
        # Otorgar recompensas
        return self.otorgar_recompensas_mision(personaje_id, mision_id)
    
    def cancelar_mision(self, personaje_id, mision_id):
        """Cancela una misión asignada"""
        # Buscar la relación personaje-misión
        personaje_mision = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id,
            mision_id=mision_id
        ).first()
        
        if not personaje_mision:
            raise ValueError(f"La misión {mision_id} no está asignada al personaje {personaje_id}")
        
        # Actualizar estado de la misión
        personaje_mision.estado = 'cancelada'
        personaje_mision.fecha_finalizacion = datetime.now()
        
        # Incrementar contador de misiones canceladas
        return self.registrar_mision_cancelada(personaje_id, mision_id)
    
    def obtener_ranking(self, limit=10):
        """Obtiene los personajes de mayor nivel (ranking)"""
        return self.personaje_repo.obtener_ranking(limit)
