from sqlalchemy.orm import Session
from sqlalchemy import desc
from Modelos.Personaje import Personaje
from Utilidades.Excepciones import PersonajeNoEncontradoError

class PersonajeRepositorio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def crear_personaje(self, personaje_data):
        """Crea un nuevo personaje en la base de datos"""
        nuevo_personaje = Personaje(**personaje_data)
        self.db_session.add(nuevo_personaje)
        self.db_session.commit()
        self.db_session.refresh(nuevo_personaje)
        return nuevo_personaje
    
    def obtener_personaje_por_id(self, personaje_id):
        """Obtiene un personaje por su ID"""
        personaje = self.db_session.query(Personaje).filter(Personaje.id == personaje_id).first()
        if not personaje:
            raise PersonajeNoEncontradoError(f"No se encontró el personaje con ID {personaje_id}")
        return personaje
    
    def obtener_todos_personajes(self, skip=0, limit=100):
        """Obtiene todos los personajes con paginación opcional"""
        return self.db_session.query(Personaje).offset(skip).limit(limit).all()
    
    def actualizar_personaje(self, personaje_id, personaje_data):
        """Actualiza un personaje existente"""
        personaje = self.obtener_personaje_por_id(personaje_id)
        for key, value in personaje_data.items():
            setattr(personaje, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(personaje)
        return personaje
    
    def eliminar_personaje(self, personaje_id):
        """Elimina un personaje de la base de datos"""
        personaje = self.obtener_personaje_por_id(personaje_id)
        self.db_session.delete(personaje)
        self.db_session.commit()
        return {"mensaje": f"Personaje {personaje_id} eliminado"}
    
    def obtener_ranking(self, limit=10):
        """Obtiene los personajes ordenados por nivel (ranking)"""
        return self.db_session.query(Personaje).order_by(
            desc(Personaje.nivel), 
            desc(Personaje.experiencia)
        ).limit(limit).all()
