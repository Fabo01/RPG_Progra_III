from sqlalchemy import Column, Integer, String, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from Modelos.Base import Base

class Mision(Base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)
    # Asegurar que tipo sea uno de los valores permitidos con el correcto ordenamiento de dificultad
    # sigilo=combate > rescate > escolta > exploracion > recoleccion
    tipo = Column(
        Enum('sigilo', 'combate', 'rescate', 'escolta', 'exploracion', 'recoleccion'), 
        nullable=False,
        default='combate'
    )
    categoria = Column(
        Enum('principal', 'secundaria'), 
        nullable=False, 
        default='secundaria'
    )
    estado = Column(
        Enum('pendiente', 'completada', 'cancelada'), 
        nullable=False, 
        default='pendiente'
 )
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False) 
    fecha_limite = Column(DateTime, nullable=True)
    dificultad = Column(Integer, nullable=False)  # 1 a 10
    experiencia = Column(Float, nullable=False) # experiencia base de la mision
    recompensa_oro = Column(Float, nullable=False)  # Recompensa en oro base de la mision

    personajes = relationship("PersonajesMisiones", back_populates="mision")  # Relación muchos a muchos con personajes