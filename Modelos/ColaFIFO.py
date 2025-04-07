from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from Modelos.Base import Base

class ColaFIFO(Base):
    __tablename__ = 'colas_fifo'
    id = Column(Integer, primary_key=True)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), nullable=False)
    tipo_cola = Column(String, nullable=False)  # 'principal' o 'secundaria'
    misiones_orden = Column(JSON, nullable=False, default=[])  # Lista ordenada de IDs de misiones
    
    # Relación con el personaje propietario de la cola
    personaje = relationship("Personaje", back_populates="colas")

