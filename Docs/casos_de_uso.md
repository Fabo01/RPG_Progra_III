# Casos de Uso - Sistema RPG de Misiones

Este documento describe todos los casos de uso del sistema RPG, proporcionando una visión completa de la funcionalidad disponible.

**Total de Casos de Uso: 27**

## Índice
1. [Actores del Sistema](#1-actores-del-sistema)
2. [Gestión de Personajes](#2-gestión-de-personajes) *(6 casos de uso)*
3. [Gestión de Misiones](#3-gestión-de-misiones) *(8 casos de uso)*
4. [Gestión de Asignación y Progreso](#4-gestión-de-asignación-y-progreso) *(6 casos de uso)*
5. [Gestión de Colas de Misiones](#5-gestión-de-colas-de-misiones) *(2 casos de uso)*
6. [Consultas y Reportes](#6-consultas-y-reportes) *(3 casos de uso)*
7. [Administración del Sistema](#7-administración-del-sistema) *(2 casos de uso)*

---

## 1. Actores del Sistema

### 1.1 Usuario
Actor principal que interactúa con el sistema para gestionar personajes, misiones y progreso en el juego.

### 1.2 Administrador
Actor con permisos extendidos para la gestión del sistema, incluyendo la creación y mantenimiento de misiones.

---

## 2. Gestión de Personajes

### CU-P01: Crear Personaje
**Actor:** Usuario  
**Descripción:** Permite al usuario crear un nuevo personaje con estadísticas iniciales predefinidas.  
**Endpoint:** `POST /personajes`

### CU-P02: Obtener Personaje
**Actor:** Usuario  
**Descripción:** Permite consultar la información detallada de un personaje específico.  
**Endpoint:** `GET /personajes/{personaje_id}`

### CU-P03: Listar Personajes
**Actor:** Usuario  
**Descripción:** Permite obtener una lista paginada de todos los personajes registrados.  
**Endpoint:** `GET /personajes?skip={skip}&limit={limit}`

### CU-P04: Actualizar Personaje
**Actor:** Usuario  
**Descripción:** Permite modificar los atributos de un personaje existente.  
**Endpoint:** `PATCH /personajes/{personaje_id}`

### CU-P05: Eliminar Personaje
**Actor:** Usuario  
**Descripción:** Permite eliminar permanentemente un personaje con todos sus datos asociados.  
**Endpoint:** `DELETE /personajes/{personaje_id}`

### CU-P06: Consultar Ranking de Personajes
**Actor:** Usuario  
**Descripción:** Permite ver una lista de personajes ordenados por nivel y experiencia.  
**Endpoint:** `GET /personajes/ranking?limit={limit}`

---

## 3. Gestión de Misiones

### CU-M01: Crear Misión
**Actor:** Administrador  
**Descripción:** Permite crear una nueva misión con sus atributos, tipo, categoría y recompensas.  
**Endpoint:** `POST /misiones`

### CU-M02: Obtener Misión
**Actor:** Usuario  
**Descripción:** Permite consultar la información detallada de una misión específica.  
**Endpoint:** `GET /misiones/{mision_id}`

### CU-M03: Listar Misiones
**Actor:** Usuario  
**Descripción:** Permite obtener una lista paginada de todas las misiones disponibles.  
**Endpoint:** `GET /misiones?skip={skip}&limit={limit}`

### CU-M04: Filtrar Misiones por Tipo
**Actor:** Usuario  
**Descripción:** Permite listar misiones filtradas por su tipo (combate, sigilo, etc.).  
**Endpoint:** `GET /misiones?tipo={tipo}&skip={skip}&limit={limit}`

### CU-M05: Filtrar Misiones por Categoría
**Actor:** Usuario  
**Descripción:** Permite listar misiones filtradas por su categoría (principal o secundaria).  
**Endpoint:** `GET /misiones?categoria={categoria}&skip={skip}&limit={limit}`

### CU-M06: Filtrar Misiones por Dificultad
**Actor:** Usuario  
**Descripción:** Permite listar misiones dentro de un rango de dificultad especificado.  
**Endpoint:** `GET /misiones?dificultad_min={min}&dificultad_max={max}&skip={skip}&limit={limit}`

### CU-M07: Actualizar Misión
**Actor:** Administrador  
**Descripción:** Permite modificar los atributos de una misión existente.  
**Endpoint:** `PATCH /misiones/{mision_id}`

### CU-M08: Eliminar Misión
**Actor:** Administrador  
**Descripción:** Permite eliminar permanentemente una misión del sistema.  
**Endpoint:** `DELETE /misiones/{mision_id}`

---

## 4. Gestión de Asignación y Progreso

### CU-A01: Asignar Misión a Personaje
**Actor:** Usuario  
**Descripción:** Permite asignar una misión a un personaje específico y encolarla según su categoría.  
**Endpoint:** `POST /personajes-misiones/asignar/{mision_id}/a/{personaje_id}`

### CU-A02: Completar Misión
**Actor:** Usuario  
**Descripción:** Marca una misión como completada, otorgando recompensas ajustadas por tipo y dificultad.  
**Endpoint:** `POST /personajes-misiones/completar/{mision_id}/personaje/{personaje_id}`

### CU-A03: Completar Primera Misión en Cola
**Actor:** Usuario  
**Descripción:** Completa la primera misión disponible en la cola (principal o secundaria).  
**Endpoint:** `POST /personajes/{personaje_id}/completar`

### CU-A04: Cancelar Misión
**Actor:** Usuario  
**Descripción:** Marca una misión como cancelada para un personaje, desacolándola si está en la cola.  
**Endpoint:** `POST /personajes-misiones/cancelar/{mision_id}/personaje/{personaje_id}`

### CU-A05: Listar Misiones de Personaje
**Actor:** Usuario  
**Descripción:** Obtiene todas las misiones asignadas a un personaje con filtro opcional por estado.  
**Endpoint:** `GET /personajes-misiones/personaje/{personaje_id}/misiones?estado={estado}`

### CU-A06: Listar Personajes por Misión
**Actor:** Usuario  
**Descripción:** Obtiene todos los personajes que tienen asignada una misión específica.  
**Endpoint:** `GET /personajes-misiones/mision/{mision_id}/personajes?estado={estado}`

---

## 5. Gestión de Colas de Misiones

### CU-C01: Consultar Cola de Misiones
**Actor:** Usuario  
**Descripción:** Obtiene información sobre el estado de una cola de misiones (principal o secundaria).  
**Endpoint:** `GET /personajes-misiones/personaje/{personaje_id}/cola/{tipo_cola}`

### CU-C02: Obtener Misiones en Orden FIFO
**Actor:** Usuario  
**Descripción:** Lista todas las misiones de un personaje ordenadas según su posición en las colas.  
**Endpoint:** `GET /personajes/{personaje_id}/misiones`

---

## 6. Consultas y Reportes

### CU-R01: Obtener Estadísticas de Personaje
**Actor:** Usuario  
**Descripción:** Consulta estadísticas detalladas de un personaje: nivel, experiencia, oro, misiones completadas.  
**Endpoint:** `GET /personajes/{personaje_id}`

### CU-R02: Obtener Historial de Misiones
**Actor:** Usuario  
**Descripción:** Obtiene un historial de todas las misiones realizadas por un personaje.  
**Endpoint:** `GET /personajes-misiones/personaje/{personaje_id}/misiones`

### CU-R03: Consultar Recompensas Potenciales
**Actor:** Usuario  
**Descripción:** Permite ver las recompensas disponibles por completar una misión específica.  
**Endpoint:** (Funcionalidad implícita al consultar detalles de una misión)

---

## 7. Administración del Sistema

### CU-S01: Inicialización del Sistema
**Actor:** Sistema  
**Descripción:** Inicializa el sistema y crea las tablas de base de datos si no existen.  
**Funcionalidad:** Ejecutada automáticamente al inicio de la aplicación.

### CU-S02: Consultar Documentación API
**Actor:** Desarrollador  
**Descripción:** Accede a la documentación interactiva de la API (Swagger).  
**Endpoint:** `GET /docs`

---

## Relaciones entre Casos de Uso

### Flujo Básico del Juego
1. El usuario crea un personaje (CU-P01)
2. El usuario explora las misiones disponibles (CU-M03, CU-M04, CU-M05, CU-M06)
3. El usuario acepta una misión (CU-A01)
4. El usuario completa la misión (CU-A02) o la siguiente en la cola (CU-A03)
5. El personaje recibe recompensas y experiencia
6. El usuario verifica su progreso (CU-R01) y clasificación (CU-P06)
7. El ciclo se repite desde el paso 2

### Flujo de Administración
1. El administrador crea nuevas misiones (CU-M01)
2. El administrador actualiza misiones existentes (CU-M07)
3. El administrador monitorea la actividad de los personajes (CU-A05, CU-A06)
4. El administrador puede eliminar misiones obsoletas (CU-M08)

### Gestión de Cola de Misiones
1. El usuario asigna una misión a un personaje (CU-A01)
2. La misión se encola automáticamente según su categoría
3. El usuario consulta su cola de misiones (CU-C01)
4. El usuario completa la primera misión de la cola (CU-A03)
5. El sistema actualiza el estado y otorga recompensas
