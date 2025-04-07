from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

# Importar la configuración de base de datos y los routers
from Config.db import crear_tablas
from API.Rutas.Personaje_Ruta import router as personaje_router
from API.Rutas.Mision_Ruta import router as mision_router
from API.Rutas.PersonajeMision import router as personaje_mision_router

# Crear la aplicación FastAPI con metadatos personalizados
app = FastAPI(
    title="Sistema RPG de Misiones",
    description="API para gestionar un sistema RPG con personajes, misiones y colas FIFO",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limita a orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la base de datos al iniciar la aplicación
@app.on_event("startup")
async def startup_db():
    crear_tablas()
    print("🚀 Base de datos inicializada correctamente")

# Incluir los routers de la API
app.include_router(personaje_router)
app.include_router(mision_router)
app.include_router(personaje_mision_router)

# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
async def root():
    return {
        "mensaje": "Sistema RPG de Misiones API está en funcionamiento",
        "documentacion": "/docs",
        "endpoints_principales": [
            {"ruta": "/personajes", "descripción": "Gestión de personajes"},
            {"ruta": "/misiones", "descripción": "Gestión de misiones"},
            {"ruta": "/personajes-misiones", "descripción": "Asignación y progreso de misiones"}
        ]
    }

# Personalizar Swagger UI (opcional)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Sistema RPG de Misiones",
        version="1.0.0",
        description="API para gestionar un sistema RPG con personajes, misiones y colas FIFO",
        routes=app.routes,
    )
    
    # Personalizar aquí si necesitas cambios específicos en la documentación OpenAPI
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Si ejecutamos este archivo directamente
if __name__ == "__main__":
    import uvicorn
    print("⚔️ Iniciando Sistema RPG de Misiones...")
    print("📚 Documentación Swagger disponible en: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
