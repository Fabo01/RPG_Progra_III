from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship
from Modelos.Base import Base

class Personaje(Base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False, default=1)
    experiencia = Column(Integer, nullable=False, default=0)
    salud = Column(Integer, nullable=False, default=100)
    mana = Column(Integer, nullable=False, default=100)
    oro = Column(Float, nullable=False, default=0.0)
    misiones_completadas = Column(Integer, nullable=False, default=0)  # Contador simple de misiones completadas
    misiones_canceladas = Column(Integer, nullable=False, default=0)  # Contador simple de misiones canceladas

    # Relaciones
    misiones = relationship("PersonajesMisiones", back_populates="personaje")  # Relación muchos a muchos con misiones
    colas = relationship("ColaFIFO", back_populates="personaje")  # Relación con sus colas de misiones
    
    def ganar_experiencia(self, cantidad):
        """Añade experiencia al personaje y sube de nivel si corresponde"""
        self.experiencia += cantidad
        # Verificar si sube de nivel (fórmula simple: nivel*100 exp para subir)
        exp_necesaria = self.nivel * 100
        if self.experiencia >= exp_necesaria:
            self.subir_nivel()
            # Restamos la experiencia usada para el nivel
            self.experiencia -= exp_necesaria
    
    def subir_nivel(self):
        """Sube de nivel al personaje y ajusta sus estadísticas"""
        self.nivel += 1
        # Incremento de estadísticas base por nivel
        self.salud += 10
        self.mana += 5
    
    def ganar_oro(self, cantidad):
        """Añade oro al personaje"""
        self.oro += cantidad