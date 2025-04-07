from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from Modelos.Base import Base

class PersonajesMisiones(Base):  # tabla intermedia para la relación muchos a muchos entre misiones y personajes
    __tablename__ = 'misiones_personajes'
    mision_id = Column(Integer, ForeignKey('misiones.id'), primary_key=True, nullable=False)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), primary_key=True, nullable=False)
    estado = Column(Enum('pendiente', 'completada', 'cancelada'), nullable=False, default='pendiente')
    fecha_asignacion = Column(DateTime, nullable=False)  # Fecha en que se asignó la misión al personaje
    fecha_finalizacion = Column(DateTime, nullable=True)  # Fecha en que se completó, fracasó o canceló la misión

    personaje = relationship('Personaje', back_populates='misiones')  # Relación muchos a muchos con personajes
    mision = relationship('Mision', back_populates='personajes')  # Relación muchos a muchos con misiones
