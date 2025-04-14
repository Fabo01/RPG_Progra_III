from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from Modelos.Base import Base

class ColaFIFO(Base):
    __tablename__ = 'colas_fifo'
    id = Column(Integer, primary_key=True)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), nullable=False)
    tipo_cola = Column(Enum('principal', 'secundaria'), nullable=False)  # Solo permite 'principal' o 'secundaria'
    misiones_orden = Column(JSON, nullable=False, default=[])
    
    # Relación con el personaje propietario de la cola
    personaje = relationship("Personaje", back_populates="colas")
