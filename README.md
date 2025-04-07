# 🎮 Sistema RPG de Misiones

Un sistema de gestión de misiones para juegos de rol (RPG), implementado como una API REST con FastAPI y SQLAlchemy.

![Versión](https://img.shields.io/badge/versión-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-orange.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)

## 📋 Contenido

- [Introducción](#introducción)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Entidades Principales](#entidades-principales)
- [Ejemplos](#ejemplos)
- [Documentación de API](#documentación-de-api)
- [Patrones de Diseño](#patrones-de-diseño)
- [Para Desarrolladores](#para-desarrolladores)

## 🔍 Introducción

El Sistema RPG de Misiones es una plataforma que permite gestionar personajes, misiones y su progreso en un juego de rol. El sistema implementa un mecanismo de colas FIFO (First In, First Out) para gestionar las misiones asignadas a los personajes, diferenciando entre misiones principales y secundarias.

### Características principales

- Gestión completa de **personajes** con estadísticas (nivel, experiencia, oro)
- Creación y gestión de **misiones** con diferentes tipos y categorías
- **Sistema de recompensas** con multiplicadores según tipo y dificultad
- **Colas FIFO** para organizar misiones por prioridad (principales/secundarias)
- **API REST** completa para integración con frontend o otros sistemas
- **Documentación interactiva** con Swagger UI

## 🏗️ Arquitectura

El sistema está implementado siguiendo una arquitectura por capas:

1. **API (FastAPI)**: Maneja las peticiones HTTP y respuestas
2. **Servicios**: Implementa la lógica de negocio
3. **Repositorios**: Encapsula el acceso a datos
4. **Modelos**: Define la estructura de datos
5. **TDA Cola**: Implementa la estructura de datos Cola para las misiones

### Estructura de directorios

```
RPG/
├── API/
│   ├── DTOs/         # Objetos de transferencia de datos
│   └── Rutas/        # Endpoints de API
├── Config/           # Configuración de la aplicación
├── Docs/             # Documentación adicional
├── Estructuras/      # Implementación de estructuras de datos
├── Modelos/          # Modelos de base de datos (ORM)
├── Repositorios/     # Acceso a datos
├── Servicios/        # Lógica de negocio
└── Utilidades/       # Funciones auxiliares
```

## 📋 Requisitos

- Python 3.7+
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/rpg-misiones.git
cd rpg-misiones
```

2. Crea y activa un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Inicia la aplicación:
```bash
python main.py
```

La API estará disponible en `http://127.0.0.1:8000` y la documentación en `http://127.0.0.1:8000/docs`.

## 🎮 Uso

### Crear un personaje

```bash
curl -X POST "http://127.0.0.1:8000/personajes/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Gandalf"}'
```

### Crear una misión

```bash
curl -X POST "http://127.0.0.1:8000/misiones/" \
     -H "Content-Type: application/json" \
     -d '{
           "nombre": "La torre oscura",
           "descripcion": "Derrotar al nigromante en la torre",
           "tipo": "combate",
           "categoria": "principal",
           "dificultad": 8,
           "experiencia": 500,
           "recompensa_oro": 1000
         }'
```

### Asignar una misión a un personaje

```bash
curl -X POST "http://127.0.0.1:8000/personajes-misiones/asignar/1/a/1"
```

### Completar una misión

```bash
curl -X POST "http://127.0.0.1:8000/personajes-misiones/completar/1/personaje/1"
```

## 🧩 Entidades Principales

### Personaje

Representa al protagonista controlado por el usuario:

- **Estadísticas**: nivel, experiencia, salud, maná, oro
- **Contadores**: misiones completadas y canceladas
- **Comportamiento**: subir de nivel, recibir recompensas

### Misión

Representa una tarea que debe completar un personaje:

- **Clasificación**: tipo (combate, sigilo, etc.) y categoría (principal/secundaria)
- **Dificultad**: escala de 1-10
- **Recompensas**: experiencia y oro base
- **Temporalidad**: fecha de creación y fecha límite (opcional)

### Cola FIFO

Estructura de datos que sigue el principio First-In-First-Out:

- **Cola principal**: para misiones de categoría "principal"
- **Cola secundaria**: para misiones de categoría "secundaria"

## 📝 Ejemplos

### Flujo de juego básico

1. Crear un personaje
2. Explorar misiones disponibles
3. Aceptar una misión (se añade a la cola correspondiente)
4. Completar la misión (se desencolada y se otorgan recompensas)
5. Ganar experiencia y subir de nivel
6. Repetir

### Sistema de recompensas

Las recompensas se calculan utilizando varios multiplicadores:

- **Multiplicador por tipo de misión**:
  - Sigilo: 1.5x
  - Combate: 1.5x
  - Rescate: 1.3x
  - Escolta: 1.2x
  - Exploración: 1.1x
  - Recolección: 1.0x

- **Multiplicador por dificultad**: 1 + (dificultad * 0.1)

Recompensa final = Recompensa base * Multiplicador tipo * Multiplicador dificultad

## 📚 Documentación de API

La API está completamente documentada con OpenAPI/Swagger:

- **Documentación interactiva**: http://127.0.0.1:8000/docs
- **Formato OpenAPI**: http://127.0.0.1:8000/openapi.json

## 🧠 Patrones de Diseño

El sistema implementa varios patrones de diseño:

- **Repositorio**: Abstrae el acceso a datos
- **Servicio**: Centraliza la lógica de negocio
- **DTO (Data Transfer Object)**: Valida y estructura los datos de entrada/salida
- **TDA (Tipo de Dato Abstracto)**: Implementa la estructura Cola

## 👨‍💻 Para Desarrolladores

### Estructura de la base de datos

El sistema utiliza SQLite con los siguientes modelos:

- **Personaje**: Almacena datos de personajes
- **Mision**: Almacena datos de misiones
- **PersonajesMisiones**: Relación muchos a muchos con estado y fechas
- **ColaFIFO**: Estructura de persistencia para las colas de misiones

### Ejecutar en modo desarrollo

```bash
uvicorn main:app --reload
```

### Extensibilidad

El sistema está diseñado para ser fácilmente extensible:

- Agregar nuevos tipos de misiones
- Implementar nuevas estadísticas para personajes
- Expandir el sistema de recompensas
- Añadir nuevos endpoints

---