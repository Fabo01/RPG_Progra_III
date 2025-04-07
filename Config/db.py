from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Modelos.Base import Base

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///rpg_game.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para crear todas las tablas
def crear_tablas():
    Base.metadata.create_all(bind=engine)

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
