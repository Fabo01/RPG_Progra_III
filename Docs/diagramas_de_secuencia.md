# Diagramas de Secuencia - Sistema RPG de Misiones

Este documento presenta los diagramas de secuencia para los principales casos de uso del sistema RPG, mostrando la interacción entre componentes.

**Total de Casos de Uso Documentados: 27**

## Índice
- [1. Gestión de Personajes](#1-gestión-de-personajes)
- [2. Gestión de Misiones](#2-gestión-de-misiones)
- [3. Gestión de Asignación y Progreso](#3-gestión-de-asignación-y-progreso)
- [4. Gestión de Colas de Misiones](#4-gestión-de-colas-de-misiones)
- [5. Consultas y Reportes](#5-consultas-y-reportes)
- [6. Administración del Sistema](#6-administración-del-sistema)

---

## 1. Gestión de Personajes

### 1.1 CU-P01: Crear Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant Servicio as PersonajeServicio
    participant Repo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: POST /personajes {nombre: "Gandalf"}
    API->>Servicio: crear_personaje(dto)
    Servicio->>Servicio: Preparar personaje_data
    Servicio->>Repo: crear_personaje(personaje_data)
    Repo->>BD: add(nuevo_personaje)
    Repo->>BD: commit()
    Repo->>BD: refresh(nuevo_personaje)
    BD-->>Repo: Personaje actualizado
    Repo-->>Servicio: Personaje creado
    Servicio-->>API: Personaje creado
    API-->>Usuario: 201 Created + Datos del personaje
```

### 1.2 CU-P02: Obtener Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant Servicio as PersonajeServicio
    participant Repo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes/{personaje_id}
    API->>Servicio: obtener_personaje(personaje_id)
    Servicio->>Repo: obtener_personaje_por_id(personaje_id)
    Repo->>BD: query(Personaje).filter(id = personaje_id)
    BD-->>Repo: Personaje o None
    
    alt Personaje encontrado
        Repo-->>Servicio: Personaje
        Servicio-->>API: Personaje
        API-->>Usuario: 200 OK + Datos del personaje
    else Personaje no encontrado
        Repo->>Servicio: raise PersonajeNoEncontradoError
        Servicio->>API: raise PersonajeNoEncontradoError
        API->>API: raise HTTPException(404)
        API-->>Usuario: 404 Not Found + Mensaje de error
    end
```

### 1.3 CU-P03: Listar Personajes

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant Servicio as PersonajeServicio
    participant Repo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes?skip=0&limit=100
    API->>Servicio: obtener_todos_personajes(skip, limit)
    Servicio->>Repo: obtener_todos_personajes(skip, limit)
    Repo->>BD: query(Personaje).offset(skip).limit(limit)
    BD-->>Repo: Lista de personajes
    Repo-->>Servicio: Lista de personajes
    Servicio-->>API: Lista de personajes
    API-->>Usuario: 200 OK + Lista de personajes
```

### 1.4 CU-P04: Actualizar Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant Servicio as PersonajeServicio
    participant Repo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: PATCH /personajes/{personaje_id} {datos actualizados}
    API->>Servicio: actualizar_personaje(personaje_id, dto)
    Servicio->>Repo: actualizar_personaje(personaje_id, datos)
    Repo->>Repo: obtener_personaje_por_id(personaje_id)
    Repo->>BD: query(Personaje).filter(id = personaje_id)
    
    alt Personaje encontrado
        BD-->>Repo: Personaje
        Repo->>BD: actualizar atributos
        Repo->>BD: commit()
        Repo->>BD: refresh(personaje)
        BD-->>Repo: Personaje actualizado
        Repo-->>Servicio: Personaje actualizado
        Servicio-->>API: Personaje actualizado
        API-->>Usuario: 200 OK + Datos del personaje actualizados
    else Personaje no encontrado
        Repo->>Servicio: raise PersonajeNoEncontradoError
        Servicio->>API: raise PersonajeNoEncontradoError
        API->>API: raise HTTPException(404)
        API-->>Usuario: 404 Not Found + Mensaje de error
    end
```

### 1.5 CU-P05: Eliminar Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant Servicio as PersonajeServicio
    participant Repo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: DELETE /personajes/{personaje_id}
    API->>Servicio: eliminar_personaje(personaje_id)
    Servicio->>Repo: eliminar_personaje(personaje_id)
    Repo->>Repo: obtener_personaje_por_id(personaje_id)
    Repo->>BD: query(Personaje).filter(id = personaje_id)
    
    alt Personaje encontrado
        BD-->>Repo: Personaje
        Repo->>BD: delete(personaje)
        Repo->>BD: commit()
        BD-->>Repo: OK
        Repo-->>Servicio: Mensaje de confirmación
        Servicio-->>API: Mensaje de confirmación
        API-->>Usuario: 200 OK + Mensaje de confirmación
    else Personaje no encontrado
        Repo->>Servicio: raise PersonajeNoEncontradoError
        Servicio->>API: raise PersonajeNoEncontradoError
        API->>API: raise HTTPException(404)
        API-->>Usuario: 404 Not Found + Mensaje de error
    end
```

### 1.6 CU-P06: Consultar Ranking de Personajes

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant Servicio as PersonajeServicio
    participant Repo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes/ranking?limit=10
    API->>Servicio: obtener_ranking(limit)
    Servicio->>Repo: obtener_ranking(limit)
    Repo->>BD: query(Personaje).order_by(nivel, experiencia).limit(limit)
    BD-->>Repo: Lista de personajes ordenada
    Repo-->>Servicio: Lista de personajes ordenada
    Servicio-->>API: Lista de personajes ordenada
    API-->>Usuario: 200 OK + Ranking de personajes
```

## 2. Gestión de Misiones

### 2.1 CU-M01: Crear Misión

```mermaid
sequenceDiagram
    participant Admin as Administrador
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Admin->>API: POST /misiones {...datos misión...}
    API->>Servicio: crear_mision(dto)
    Servicio->>Servicio: mision_data = dto.dict()
    Servicio->>Servicio: Añadir fecha_creacion y estado
    Servicio->>Repo: crear_mision(mision_data)
    Repo->>BD: add(nueva_mision)
    Repo->>BD: commit()
    Repo->>BD: refresh(nueva_mision)
    BD-->>Repo: Misión actualizada
    Repo-->>Servicio: Misión creada
    Servicio-->>API: Misión creada
    API-->>Admin: 201 Created + Datos de la misión
```

### 2.2 CU-M02: Obtener Misión

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /misiones/{mision_id}
    API->>Servicio: obtener_mision(mision_id)
    Servicio->>Repo: obtener_mision_por_id(mision_id)
    Repo->>BD: query(Mision).filter(id = mision_id)
    BD-->>Repo: Misión o None
    
    alt Misión encontrada
        Repo-->>Servicio: Misión
        Servicio-->>API: Misión
        API-->>Usuario: 200 OK + Datos de la misión
    else Misión no encontrada
        Repo->>Servicio: raise MisionNoEncontradaError
        Servicio->>API: raise MisionNoEncontradaError
        API->>API: raise HTTPException(404)
        API-->>Usuario: 404 Not Found + Mensaje de error
    end
```

### 2.3 CU-M03: Listar Misiones

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /misiones?skip=0&limit=100
    API->>Servicio: obtener_todas_misiones(skip, limit)
    Servicio->>Repo: obtener_todas_misiones(skip, limit)
    Repo->>BD: query(Mision).offset(skip).limit(limit)
    BD-->>Repo: Lista de misiones
    Repo-->>Servicio: Lista de misiones
    Servicio-->>API: Lista de misiones
    API-->>Usuario: 200 OK + Lista de misiones
```

### 2.4 CU-M04: Filtrar Misiones por Tipo

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /misiones?tipo=combate&skip=0&limit=100
    API->>Servicio: obtener_misiones_por_tipo(tipo, skip, limit)
    Servicio->>Repo: obtener_misiones_por_tipo(tipo, skip, limit)
    Repo->>BD: query(Mision).filter(tipo=tipo).offset(skip).limit(limit)
    BD-->>Repo: Lista de misiones filtradas
    Repo-->>Servicio: Lista de misiones filtradas
    Servicio-->>API: Lista de misiones filtradas
    API-->>Usuario: 200 OK + Lista de misiones filtradas
```

### 2.5 CU-M05: Filtrar Misiones por Categoría

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /misiones?categoria=principal&skip=0&limit=100
    API->>Servicio: obtener_misiones_por_categoria(categoria, skip, limit)
    Servicio->>Repo: obtener_misiones_por_categoria(categoria, skip, limit)
    Repo->>BD: query(Mision).filter(categoria=categoria).offset(skip).limit(limit)
    BD-->>Repo: Lista de misiones filtradas
    Repo-->>Servicio: Lista de misiones filtradas
    Servicio-->>API: Lista de misiones filtradas
    API-->>Usuario: 200 OK + Lista de misiones filtradas
```

### 2.6 CU-M06: Filtrar Misiones por Dificultad

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /misiones?dificultad_min=3&dificultad_max=7&skip=0&limit=100
    API->>Servicio: obtener_misiones_por_dificultad(min, max, skip, limit)
    Servicio->>Repo: obtener_misiones_por_dificultad(min, max, skip, limit)
    Repo->>BD: query(Mision).filter(dificultad ≥ min, dificultad ≤ max).offset(skip).limit(limit)
    BD-->>Repo: Lista de misiones filtradas
    Repo-->>Servicio: Lista de misiones filtradas
    Servicio-->>API: Lista de misiones filtradas
    API-->>Usuario: 200 OK + Lista de misiones filtradas
```

### 2.7 CU-M07: Actualizar Misión

```mermaid
sequenceDiagram
    participant Admin
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Admin->>API: PATCH /misiones/{mision_id} {datos actualizados}
    API->>Servicio: actualizar_mision(mision_id, dto)
    Servicio->>Repo: actualizar_mision(mision_id, datos)
    Repo->>Repo: obtener_mision_por_id(mision_id)
    Repo->>BD: query(Mision).filter(id = mision_id)
    
    alt Misión encontrada
        BD-->>Repo: Misión
        Repo->>BD: actualizar atributos
        Repo->>BD: commit()
        Repo->>BD: refresh(mision)
        BD-->>Repo: Misión actualizada
        Repo-->>Servicio: Misión actualizada
        Servicio-->>API: Misión actualizada
        API-->>Admin: 200 OK + Datos de la misión actualizados
    else Misión no encontrada
        Repo->>Servicio: raise MisionNoEncontradaError
        Servicio->>API: raise MisionNoEncontradaError
        API->>API: raise HTTPException(404)
        API-->>Admin: 404 Not Found + Mensaje de error
    end
```

### 2.8 CU-M08: Eliminar Misión

```mermaid
sequenceDiagram
    participant Admin
    participant API as API (Mision_Ruta)
    participant Servicio as MisionServicio
    participant Repo as MisionRepositorio
    participant BD as Base de Datos

    Admin->>API: DELETE /misiones/{mision_id}
    API->>Servicio: eliminar_mision(mision_id)
    Servicio->>Repo: eliminar_mision(mision_id)
    Repo->>Repo: obtener_mision_por_id(mision_id)
    Repo->>BD: query(Mision).filter(id = mision_id)
    
    alt Misión encontrada
        BD-->>Repo: Misión
        Repo->>BD: delete(mision)
        Repo->>BD: commit()
        BD-->>Repo: OK
        Repo-->>Servicio: Mensaje de confirmación
        Servicio-->>API: Mensaje de confirmación
        API-->>Admin: 200 OK + Mensaje de confirmación
    else Misión no encontrada
        Repo->>Servicio: raise MisionNoEncontradaError
        Servicio->>API: raise MisionNoEncontradaError
        API->>API: raise HTTPException(404)
        API-->>Admin: 404 Not Found + Mensaje de error
    end
```

## 3. Gestión de Asignación y Progreso

### 3.1 CU-A01: Asignar Misión a Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant MServ as MisionServicio
    participant MRepo as MisionRepositorio
    participant PMRepo as PersonajeMisionRepositorio
    participant ColaServ as ColaServicio
    participant BD as Base de Datos

    Usuario->>API: POST /personajes-misiones/asignar/{mision_id}/a/{personaje_id}
    API->>MServ: asignar_mision_a_personaje(mision_id, personaje_id)
    MServ->>MRepo: obtener_mision_por_id(mision_id)
    MRepo->>BD: query(Mision)
    BD-->>MRepo: Misión
    MRepo-->>MServ: Misión
    
    MServ->>PMRepo: asignar_mision(personaje_id, mision_id)
    PMRepo->>BD: Buscar relación existente
    BD-->>PMRepo: Resultado
    
    alt Relación no existe
        PMRepo->>BD: add(nueva_asignacion)
        PMRepo->>BD: commit()
        PMRepo->>BD: refresh(nueva_asignacion)
    end
    
    PMRepo-->>MServ: Relación personaje-misión
    
    MServ->>MServ: es_principal = mision.categoria == 'principal'
    MServ->>ColaServ: encolar_mision(personaje_id, mision_id, es_principal)
    ColaServ->>ColaServ: obtener_cola_personaje()
    ColaServ->>ColaServ: cola_tda.enqueue(personaje_mision)
    ColaServ->>ColaServ: guardar_cola_personaje()
    ColaServ-->>MServ: Resultado
    
    MServ-->>API: Resultado asignación
    API-->>Usuario: 200 OK + Información de asignación
```

### 3.2 CU-A02: Completar Misión

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant MServ as MisionServicio
    participant PServ as PersonajeServicio
    participant MRepo as MisionRepositorio
    participant PMRepo as PersonajeMisionRepositorio
    participant ColaServ as ColaServicio
    participant BD as Base de Datos

    Usuario->>API: POST /personajes-misiones/completar/{mision_id}/personaje/{personaje_id}
    API->>MServ: completar_mision_personaje(mision_id, personaje_id)
    MServ->>MRepo: obtener_mision_por_id(mision_id)
    MRepo->>BD: query(Mision)
    BD-->>MRepo: Misión
    MRepo-->>MServ: Misión
    
    MServ->>MServ: es_principal = mision.categoria == 'principal'
    MServ->>ColaServ: desencolar_mision(personaje_id, es_principal)
    ColaServ->>ColaServ: obtener_cola_personaje()
    ColaServ->>ColaServ: cola_tda.dequeue()
    ColaServ->>ColaServ: guardar_cola_personaje()
    ColaServ-->>MServ: Misión desencolada
    
    MServ->>PMRepo: actualizar_estado(personaje_id, mision_id, 'completada')
    PMRepo->>BD: Actualizar estado y fecha_finalizacion
    PMRepo->>BD: commit()
    BD-->>PMRepo: OK
    PMRepo-->>MServ: Relación actualizada
    MServ-->>API: Estado actualizado
    
    API->>PServ: otorgar_recompensas_mision(personaje_id, mision_id)
    PServ->>BD: Obtener relación personaje-misión
    BD-->>PServ: Relación
    PServ->>PServ: Calcular multiplicador por tipo de misión
    PServ->>PServ: Calcular recompensas (exp, oro)
    PServ->>BD: Actualizar personaje
    PServ->>BD: commit()
    BD-->>PServ: OK
    PServ-->>API: Resultado con recompensas
    
    API-->>Usuario: 200 OK + Detalles de recompensas
```

### 3.3 CU-A03: Completar Primera Misión en Cola

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant PServ as PersonajeServicio
    participant MServ as MisionServicio
    participant ColaServ as ColaServicio
    participant PMRepo as PersonajeMisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: POST /personajes/{personaje_id}/completar
    API->>ColaServ: obtener_primera_mision(personaje_id, es_principal=true)
    ColaServ->>BD: Buscar cola principal
    BD-->>ColaServ: Cola principal
    
    alt Cola principal tiene misiones
        ColaServ-->>API: Primera misión principal
    else Cola principal vacía
        ColaServ-->>API: None
        API->>ColaServ: obtener_primera_mision(personaje_id, es_principal=false)
        ColaServ->>BD: Buscar cola secundaria
        BD-->>ColaServ: Cola secundaria
        
        alt Cola secundaria tiene misiones
            ColaServ-->>API: Primera misión secundaria
        else Cola secundaria vacía
            ColaServ-->>API: None
            API->>API: raise HTTPException(404)
            API-->>Usuario: 404 Not Found "No hay misiones pendientes"
            note right of API: Fin del flujo si no hay misiones
        end
    end
    
    API->>ColaServ: desencolar_mision(personaje_id, es_principal)
    ColaServ->>BD: Actualizar cola en BD
    BD-->>ColaServ: OK
    ColaServ-->>API: Misión desencolada
    
    API->>MServ: Obtener mision_id de la misión desencolada
    MServ-->>API: mision_id
    
    API->>PMRepo: actualizar_estado(personaje_id, mision_id, 'completada')
    PMRepo->>BD: Actualizar estado
    BD-->>PMRepo: OK
    PMRepo-->>API: OK
    
    API->>PServ: otorgar_recompensas_mision(personaje_id, mision_id)
    PServ->>PServ: Calcular recompensas con multiplicadores
    PServ->>BD: Actualizar personaje
    BD-->>PServ: OK
    PServ-->>API: Resultado con recompensas
    
    API-->>Usuario: 200 OK + Detalles de recompensas
```

### 3.4 CU-A04: Cancelar Misión

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant MServ as MisionServicio
    participant PServ as PersonajeServicio
    participant MRepo as MisionRepositorio
    participant PMRepo as PersonajeMisionRepositorio
    participant ColaServ as ColaServicio
    participant BD as Base de Datos

    Usuario->>API: POST /personajes-misiones/cancelar/{mision_id}/personaje/{personaje_id}
    API->>MServ: cancelar_mision_personaje(mision_id, personaje_id)
    MServ->>MRepo: obtener_mision_por_id(mision_id)
    MRepo->>BD: query(Mision)
    BD-->>MRepo: Misión
    MRepo-->>MServ: Misión
    
    MServ->>MServ: es_principal = mision.categoria == 'principal'
    MServ->>ColaServ: desencolar_mision(personaje_id, es_principal)
    ColaServ->>ColaServ: obtener_cola_personaje()
    ColaServ->>ColaServ: cola_tda.dequeue()
    ColaServ->>ColaServ: guardar_cola_personaje()
    ColaServ-->>MServ: Misión desencolada
    
    MServ->>PMRepo: actualizar_estado(personaje_id, mision_id, 'cancelada')
    PMRepo->>BD: Actualizar estado y fecha_finalizacion
    PMRepo->>BD: commit()
    BD-->>PMRepo: OK
    PMRepo-->>MServ: Relación actualizada
    MServ-->>API: Estado actualizado
    
    API->>PServ: registrar_mision_cancelada(personaje_id, mision_id)
    PServ->>BD: Incrementar contador misiones_canceladas
    PServ->>BD: commit()
    BD-->>PServ: OK
    PServ-->>API: Resultado
    
    API-->>Usuario: 200 OK + Confirmación de cancelación
```

### 3.5 CU-A05: Listar Misiones de Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant MServ as MisionServicio
    participant PMRepo as PersonajeMisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes-misiones/personaje/{personaje_id}/misiones?estado=pendiente
    API->>MServ: obtener_misiones_por_personaje(personaje_id, estado)
    MServ->>PMRepo: obtener_misiones_por_personaje(personaje_id, estado)
    PMRepo->>BD: query(PersonajesMisiones).filter(personaje_id, estado)
    BD-->>PMRepo: Relaciones personaje-misión
    PMRepo->>PMRepo: Extraer misiones de las relaciones
    PMRepo-->>MServ: Lista de misiones
    MServ-->>API: Lista de misiones
    API-->>Usuario: 200 OK + Lista de misiones
```

### 3.6 CU-A06: Listar Personajes por Misión

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant MServ as MisionServicio
    participant PMRepo as PersonajeMisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes-misiones/mision/{mision_id}/personajes?estado=completada
    API->>MServ: obtener_personajes_por_mision(mision_id, estado)
    MServ->>PMRepo: obtener_personajes_por_mision(mision_id, estado)
    PMRepo->>BD: query(PersonajesMisiones).filter(mision_id, estado)
    BD-->>PMRepo: Relaciones personaje-misión
    PMRepo->>PMRepo: Extraer personajes de las relaciones
    PMRepo-->>MServ: Lista de personajes
    MServ-->>API: Lista de personajes
    API-->>Usuario: 200 OK + Lista de personajes
```

## 4. Gestión de Colas de Misiones

### 4.1 CU-C01: Consultar Cola de Misiones

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant ColaServ as ColaServicio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes-misiones/personaje/{personaje_id}/cola/{tipo_cola}
    API->>API: Validar tipo_cola ('principal' o 'secundaria')
    API->>ColaServ: esta_vacia_cola(personaje_id, es_principal)
    ColaServ->>ColaServ: obtener_cola_personaje()
    ColaServ->>BD: query(ColaFIFO)
    BD-->>ColaServ: Datos de cola
    ColaServ-->>API: ¿Cola vacía?
    
    API->>ColaServ: obtener_tamano_cola(personaje_id, es_principal)
    ColaServ->>ColaServ: obtener_cola_personaje()
    ColaServ-->>API: Tamaño de cola
    
    API->>ColaServ: obtener_primera_mision(personaje_id, es_principal)
    ColaServ->>ColaServ: obtener_cola_personaje()
    ColaServ->>ColaServ: cola_tda.first()
    ColaServ-->>API: Primera misión (o null)
    
    API->>API: Preparar respuesta con la información
    API-->>Usuario: 200 OK + Información de la cola
```

### 4.2 CU-C02: Obtener Misiones en Orden FIFO

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant ColaServ as ColaServicio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes/{personaje_id}/misiones
    API->>ColaServ: obtener_cola_personaje(personaje_id, 'principal')
    ColaServ->>BD: query(ColaFIFO).filter(personaje_id, tipo='principal')
    BD-->>ColaServ: Cola principal
    ColaServ-->>API: Cola principal (TDA_Cola)
    
    API->>ColaServ: obtener_cola_personaje(personaje_id, 'secundaria')
    ColaServ->>BD: query(ColaFIFO).filter(personaje_id, tipo='secundaria')
    BD-->>ColaServ: Cola secundaria
    ColaServ-->>API: Cola secundaria (TDA_Cola)
    
    API->>API: Extraer misiones de ambas colas
    API->>API: Combinar listas (principales seguidas de secundarias)
    API-->>Usuario: 200 OK + Lista ordenada de misiones
```

## 5. Consultas y Reportes

### 5.1 CU-R01: Obtener Estadísticas de Personaje

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Personaje_Ruta)
    participant PServ as PersonajeServicio
    participant PRepo as PersonajeRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes/{personaje_id}
    API->>PServ: obtener_personaje(personaje_id)
    PServ->>PRepo: obtener_personaje_por_id(personaje_id)
    PRepo->>BD: query(Personaje).filter(id = personaje_id)
    BD-->>PRepo: Personaje o None
    
    alt Personaje encontrado
        PRepo-->>PServ: Personaje con estadísticas
        PServ-->>API: Personaje con estadísticas
        API-->>Usuario: 200 OK + Estadísticas completas
    else Personaje no encontrado
        PRepo->>PServ: raise PersonajeNoEncontradoError
        PServ->>API: raise PersonajeNoEncontradoError
        API->>API: raise HTTPException(404)
        API-->>Usuario: 404 Not Found + Mensaje de error
    end
```

### 5.2 CU-R02: Obtener Historial de Misiones

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (PersonajeMision)
    participant MServ as MisionServicio
    participant PMRepo as PersonajeMisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /personajes-misiones/personaje/{personaje_id}/misiones
    API->>MServ: obtener_misiones_por_personaje(personaje_id)
    MServ->>PMRepo: obtener_misiones_por_personaje(personaje_id)
    PMRepo->>BD: query(PersonajesMisiones).filter(personaje_id)
    BD-->>PMRepo: Todas las relaciones personaje-misión
    PMRepo->>PMRepo: Extraer misiones con estado y fechas
    PMRepo-->>MServ: Historial completo de misiones
    MServ-->>API: Historial completo de misiones
    API-->>Usuario: 200 OK + Historial de misiones
```

### 5.3 CU-R03: Consultar Recompensas Potenciales

```mermaid
sequenceDiagram
    participant Usuario
    participant API as API (Mision_Ruta)
    participant MServ as MisionServicio
    participant MRepo as MisionRepositorio
    participant BD as Base de Datos

    Usuario->>API: GET /misiones/{mision_id}
    API->>MServ: obtener_mision(mision_id)
    MServ->>MRepo: obtener_mision_por_id(mision_id)
    MRepo->>BD: query(Mision).filter(id = mision_id)
    BD-->>MRepo: Misión o None
    
    alt Misión encontrada
        MRepo-->>MServ: Misión con recompensas base
        MServ-->>API: Misión con recompensas base
        API-->>Usuario: 200 OK + Datos de misión con recompensas
    else Misión no encontrada
        MRepo->>MServ: raise MisionNoEncontradaError
        MServ->>API: raise MisionNoEncontradaError
        API->>API: raise HTTPException(404)
        API-->>Usuario: 404 Not Found + Mensaje de error
    end
```

## 6. Administración del Sistema

### 6.1 CU-S01: Inicialización del Sistema

```mermaid
sequenceDiagram
    participant Sistema
    participant App as FastAPI App
    participant BD as Base de Datos

    Sistema->>App: Iniciar aplicación
    App->>App: Evento "startup"
    App->>BD: crear_tablas()
    BD->>BD: Verificar existencia de tablas
    
    alt Tablas no existen
        BD->>BD: Base.metadata.create_all()
        BD-->>App: Tablas creadas
    else Tablas ya existen
        BD-->>App: Tablas existentes verificadas
    end
    
    App->>App: Registrar routers
    App-->>Sistema: Aplicación iniciada y lista
```

### 6.2 CU-S02: Consultar Documentación API

```mermaid
sequenceDiagram
    participant Dev as Desarrollador
    participant API as API (Docs)
    participant App as FastAPI App

    Dev->>API: GET /docs
    API->>App: get_swagger_ui_html()
    App->>App: Generar esquema OpenAPI
    App->>App: Renderizar interfaz Swagger UI
    App-->>API: HTML + JS de Swagger UI
    API-->>Dev: Documentación interactiva de la API
```

---

Los diagramas de secuencia presentados muestran cómo interactúan los diferentes componentes del sistema para implementar los casos de uso del RPG, siguiendo la arquitectura por capas establecida (API → Servicio → Repositorio → Base de Datos) y respetando los principios de separación de responsabilidades.
