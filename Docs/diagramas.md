# Diagramas del Sistema RPG

Este documento contiene todos los diagramas principales del sistema RPG, incluyendo arquitectura, patrones, clases, entidad-relación, objetos y componentes.

## Índice
1. [Diagrama de Arquitectura](#1-diagrama-de-arquitectura)
2. [Diagramas de Patrones](#2-diagramas-de-patrones)
3. [Diagrama de Clases](#3-diagrama-de-clases)
4. [Modelo Entidad-Relación](#4-modelo-entidad-relación)
5. [Diagrama de Objetos](#5-diagrama-de-objetos)
6. [Diagrama de Componentes](#6-diagrama-de-componentes)

---

## 1. Diagrama de Arquitectura

Este diagrama muestra la arquitectura en capas del sistema RPG, ilustrando la separación clara de responsabilidades y la dirección del flujo de datos.

```mermaid
graph TD
    subgraph "Capa de Presentación"
        API[API FastAPI]
        Swagger[Swagger UI]
    end

    subgraph "Capa de Servicio"
        PS[PersonajeServicio]
        MS[MisionServicio]
        CS[ColaServicio]
    end

    subgraph "Capa de Repositorio"
        PR[PersonajeRepositorio]
        MR[MisionRepositorio]
        PMR[PersonajeMisionRepositorio]
    end

    subgraph "Capa de Modelo / Dominio"
        P[Personaje]
        M[Mision]
        PM[PersonajesMisiones]
        Cola[TDA_Cola]
        ColaBD[ColaFIFO]
    end

    subgraph "Capa de Persistencia"
        DB[(Base de Datos SQLite)]
    end

    %% Conexiones entre capas
    API --> PS
    API --> MS
    API --> CS
    Swagger --> API

    PS --> PR
    MS --> MR
    MS --> PMR
    MS --> CS
    CS --> PR
    CS --> MR
    CS --> PMR

    PR --> P
    MR --> M
    PMR --> PM
    CS --> Cola
    CS --> ColaBD

    PR --> DB
    MR --> DB
    PMR --> DB
    ColaBD --> DB

    %% Estilos
    classDef api fill:#f9f,stroke:#333,stroke-width:2px;
    classDef service fill:#bbf,stroke:#333,stroke-width:1px;
    classDef repo fill:#bfb,stroke:#333,stroke-width:1px;
    classDef model fill:#fbb,stroke:#333,stroke-width:1px;
    classDef db fill:#bbb,stroke:#333,stroke-width:4px;

    class API,Swagger api;
    class PS,MS,CS service;
    class PR,MR,PMR repo;
    class P,M,PM,Cola,ColaBD model;
    class DB db;
```

El diagrama muestra nuestro sistema con una arquitectura en capas bien definida:
1. **Capa de Presentación**: API REST con FastAPI y documentación Swagger
2. **Capa de Servicio**: Implementa la lógica de negocio
3. **Capa de Repositorio**: Abstrae el acceso a datos
4. **Capa de Modelo/Dominio**: Define las entidades del sistema
5. **Capa de Persistencia**: Almacenamiento en base de datos SQLite

---

## 2. Diagramas de Patrones

### 2.1 Patrón Repositorio

```mermaid
classDiagram
    class IRepositorio~T~ {
        <<interface>>
        +crear(data)
        +obtener_por_id(id)
        +obtener_todos(skip, limit)
        +actualizar(id, data)
        +eliminar(id)
    }
    
    class PersonajeRepositorio {
        -db_session
        +crear_personaje(data)
        +obtener_personaje_por_id(id)
        +obtener_todos_personajes(skip, limit)
        +actualizar_personaje(id, data)
        +eliminar_personaje(id)
        +obtener_ranking(limit)
    }
    
    class MisionRepositorio {
        -db_session
        +crear_mision(data)
        +obtener_mision_por_id(id)
        +obtener_todas_misiones(skip, limit)
        +obtener_misiones_por_tipo(tipo, skip, limit)
        +obtener_misiones_por_categoria(categoria, skip, limit)
        +obtener_misiones_por_dificultad(min, max, skip, limit)
        +actualizar_mision(id, data)
        +eliminar_mision(id)
    }
    
    IRepositorio <|.. PersonajeRepositorio : implements
    IRepositorio <|.. MisionRepositorio : implements
    
    PersonajeServicio --> PersonajeRepositorio : uses
    MisionServicio --> MisionRepositorio : uses
```

### 2.2 Patrón Servicio

```mermaid
classDiagram
    class PersonajeServicio {
        -db_session
        -personaje_repo
        +crear_personaje(dto)
        +obtener_personaje(id)
        +obtener_todos_personajes(skip, limit)
        +actualizar_personaje(id, dto)
        +eliminar_personaje(id)
        +asignar_mision(personaje_id, mision_id)
        +otorgar_recompensas_mision(personaje_id, mision_id)
        +registrar_mision_cancelada(personaje_id, mision_id)
        +completar_mision(personaje_id, mision_id)
        +cancelar_mision(personaje_id, mision_id)
        +obtener_ranking(limit)
    }
    
    class MisionServicio {
        -db_session
        -mision_repo
        -personaje_mision_repo
        -cola_servicio
        +crear_mision(dto)
        +obtener_mision(id)
        +obtener_todas_misiones(skip, limit)
        +obtener_misiones_por_tipo(tipo, skip, limit)
        +obtener_misiones_por_categoria(categoria, skip, limit)
        +obtener_misiones_por_dificultad(min, max, skip, limit)
        +actualizar_mision(id, dto)
        +eliminar_mision(id)
        +asignar_mision_a_personaje(mision_id, personaje_id)
        +completar_mision_personaje(mision_id, personaje_id)
        +cancelar_mision_personaje(mision_id, personaje_id)
        +obtener_personajes_por_mision(mision_id, estado)
        +obtener_misiones_por_personaje(personaje_id, estado)
    }
    
    class ColaServicio {
        -db_session
        +obtener_cola_personaje(personaje_id, tipo_cola)
        +guardar_cola_personaje(personaje_id, tipo_cola, cola_tda)
        +encolar_mision(personaje_id, mision_id, es_principal)
        +desencolar_mision(personaje_id, es_principal)
        +obtener_primera_mision(personaje_id, es_principal)
        +esta_vacia_cola(personaje_id, es_principal)
        +obtener_tamano_cola(personaje_id, es_principal)
    }
    
    PersonajeServicio --> PersonajeRepositorio : uses
    MisionServicio --> MisionRepositorio : uses
    MisionServicio --> PersonajeMisionRepositorio : uses
    MisionServicio --> ColaServicio : uses
    ColaServicio ..> TDA_Cola : creates/uses
```

### 2.3 Patrón DTO (Data Transfer Object)

```mermaid
classDiagram
    class BaseModel {
        <<Pydantic>>
    }
    
    class PersonajeBase {
        +nombre: str
    }
    
    class PersonajeCreacion {
    }
    
    class PersonajeActualizacion {
        +nombre: Optional[str]
    }
    
    class PersonajeRespuesta {
        +id: int
        +nivel: int
        +experiencia: int
        +salud: int
        +mana: int
        +oro: float
        +misiones_completadas: int
        +misiones_canceladas: int
    }
    
    class MisionBase {
        +nombre: str
        +descripcion: str
        +tipo: str
        +categoria: str
        +dificultad: int
        +experiencia: float
        +recompensa_oro: float
    }
    
    class MisionCreacion {
        +fecha_limite: Optional[datetime]
    }
    
    BaseModel <|-- PersonajeBase
    PersonajeBase <|-- PersonajeCreacion
    BaseModel <|-- PersonajeActualizacion
    PersonajeBase <|-- PersonajeRespuesta
    
    BaseModel <|-- MisionBase
    MisionBase <|-- MisionCreacion
```

### 2.4 Patrón TDA (Tipo de Dato Abstracto)

```mermaid
classDiagram
    class TDA_Cola {
        -items: list
        +enqueue(item)
        +dequeue()
        +first()
        +is_empty()
        +size()
    }
    
    class ColaServicio {
        -db_session
        +obtener_cola_personaje(personaje_id, tipo_cola)
        +guardar_cola_personaje(personaje_id, tipo_cola, cola_tda)
        +encolar_mision(personaje_id, mision_id, es_principal)
        +desencolar_mision(personaje_id, es_principal)
        +obtener_primera_mision(personaje_id, es_principal)
        +esta_vacia_cola(personaje_id, es_principal)
        +obtener_tamano_cola(personaje_id, es_principal)
    }
    
    class ColaFIFO {
        +id: Integer
        +personaje_id: Integer
        +tipo_cola: String
        +misiones_orden: JSON
    }
    
    ColaServicio --> TDA_Cola : creates & uses
    ColaServicio --> ColaFIFO : persists
```

---

## 3. Diagrama de Clases

```mermaid
classDiagram
    class Base {
        <<SQLAlchemy Base>>
    }
    
    class Personaje {
        +id: Integer PK
        +nombre: String
        +nivel: Integer
        +experiencia: Integer
        +salud: Integer
        +mana: Integer
        +oro: Float
        +misiones_completadas: Integer
        +misiones_canceladas: Integer
        +ganar_experiencia(cantidad)
        +subir_nivel()
        +ganar_oro(cantidad)
    }
    
    class Mision {
        +id: Integer PK
        +tipo: Enum
        +categoria: Enum
        +estado: Enum
        +nombre: String
        +descripcion: String
        +fecha_creacion: DateTime
        +fecha_limite: DateTime
        +dificultad: Integer
        +experiencia: Float
        +recompensa_oro: Float
    }
    
    class PersonajesMisiones {
        +mision_id: Integer PK, FK
        +personaje_id: Integer PK, FK
        +estado: Enum
        +fecha_asignacion: DateTime
        +fecha_finalizacion: DateTime
    }
    
    class ColaFIFO {
        +id: Integer PK
        +personaje_id: Integer FK
        +tipo_cola: String
        +misiones_orden: JSON
    }
    
    class TDA_Cola {
        -items: list
        +enqueue(item)
        +dequeue()
        +first()
        +is_empty()
        +size()
    }
    
    Base <|-- Personaje : extends
    Base <|-- Mision : extends
    Base <|-- PersonajesMisiones : extends
    Base <|-- ColaFIFO : extends
    
    Personaje "1" -- "*" PersonajesMisiones : has
    Mision "1" -- "*" PersonajesMisiones : has
    Personaje "1" -- "*" ColaFIFO : has
    
    ColaServicio --> TDA_Cola : uses
```

---

## 4. Modelo Entidad-Relación

```mermaid
erDiagram
    PERSONAJE ||--o{ PERSONAJESMISIONES : "realiza"
    MISION ||--o{ PERSONAJESMISIONES : "es realizada por"
    PERSONAJE ||--o{ COLAFIFO : "tiene"
    
    PERSONAJE {
        int id PK
        string nombre
        int nivel
        int experiencia
        int salud
        int mana
        float oro
        int misiones_completadas
        int misiones_canceladas
    }
    
    MISION {
        int id PK
        enum tipo
        enum categoria
        enum estado
        string nombre
        string descripcion
        datetime fecha_creacion
        datetime fecha_limite
        int dificultad
        float experiencia
        float recompensa_oro
    }
    
    PERSONAJESMISIONES {
        int mision_id PK, FK
        int personaje_id PK, FK
        enum estado
        datetime fecha_asignacion
        datetime fecha_finalizacion
    }
    
    COLAFIFO {
        int id PK
        int personaje_id FK
        string tipo_cola
        json misiones_orden
    }
```

---

## 5. Diagrama de Objetos

Este diagrama muestra un ejemplo de instancias concretas de las clases del sistema y sus relaciones.

```mermaid
classDiagram
    class personaje1 {
        id = 1
        nombre = "Gandalf"
        nivel = 5
        experiencia = 450
        salud = 150
        mana = 200
        oro = 1250.75
        misiones_completadas = 12
        misiones_canceladas = 2
    }
    
    class mision1 {
        id = 5
        tipo = "combate"
        categoria = "principal"
        estado = "pendiente"
        nombre = "Derrotar al dragón"
        descripcion = "Eliminar al dragón que acecha la aldea"
        dificultad = 8
        experiencia = 500
        recompensa_oro = 1000
    }
    
    class mision2 {
        id = 8
        tipo = "recoleccion"
        categoria = "secundaria"
        estado = "pendiente"
        nombre = "Recolectar hierbas"
        descripcion = "Buscar hierbas medicinales en el bosque"
        dificultad = 3
        experiencia = 100
        recompensa_oro = 50
    }
    
    class personaje_mision1 {
        mision_id = 5
        personaje_id = 1
        estado = "pendiente"
        fecha_asignacion = "2023-10-15T10:30:00"
        fecha_finalizacion = null
    }
    
    class personaje_mision2 {
        mision_id = 8
        personaje_id = 1
        estado = "pendiente"
        fecha_asignacion = "2023-10-14T15:45:00"
        fecha_finalizacion = null
    }
    
    class cola_principal1 {
        id = 1
        personaje_id = 1
        tipo_cola = "principal"
        misiones_orden = [5]
    }
    
    class cola_secundaria1 {
        id = 2
        personaje_id = 1
        tipo_cola = "secundaria"
        misiones_orden = [8]
    }
    
    personaje1 -- personaje_mision1 : tiene
    personaje1 -- personaje_mision2 : tiene
    mision1 -- personaje_mision1 : asignada a
    mision2 -- personaje_mision2 : asignada a
    personaje1 -- cola_principal1 : tiene
    personaje1 -- cola_secundaria1 : tiene
    cola_principal1 .. mision1 : contiene
    cola_secundaria1 .. mision2 : contiene
```

---

## 6. Diagrama de Componentes

```mermaid
graph TB
    subgraph "API Layer"
        PersonajesAPI["Personajes API"]
        MisionesAPI["Misiones API"]
        PersonajesMisionesAPI["Personajes-Misiones API"]
    end
    
    subgraph "Service Layer"
        PersonajeService["PersonajeServicio"]
        MisionService["MisionServicio"]
        ColaService["ColaServicio"]
    end
    
    subgraph "Repository Layer"
        PersonajeRepo["PersonajeRepositorio"]
        MisionRepo["MisionRepositorio"]
        PersonajeMisionRepo["PersonajeMisionRepositorio"]
    end
    
    subgraph "Domain Layer"
        Personaje["Personaje"]
        Mision["Misión"]
        PersonajeMision["PersonajesMisiones"]
        Cola["TDA_Cola"]
        ColaBD["ColaFIFO"]
    end
    
    subgraph "Data Access Layer"
        DB[(SQLite Database)]
    end
    
    PersonajesAPI --> PersonajeService
    MisionesAPI --> MisionService
    PersonajesMisionesAPI --> MisionService
    PersonajesMisionesAPI --> PersonajeService
    PersonajesMisionesAPI --> ColaService
    
    PersonajeService --> PersonajeRepo
    MisionService --> MisionRepo
    MisionService --> PersonajeMisionRepo
    MisionService --> ColaService
    ColaService --> PersonajeRepo
    
    PersonajeRepo --> Personaje
    MisionRepo --> Mision
    PersonajeMisionRepo --> PersonajeMision
    ColaService --> Cola
    ColaService --> ColaBD
    
    Personaje --> DB
    Mision --> DB
    PersonajeMision --> DB
    ColaBD --> DB

    classDef apiLayer fill:#f9f,stroke:#333,stroke-width:1px;
    classDef serviceLayer fill:#bbf,stroke:#333,stroke-width:1px;
    classDef repoLayer fill:#bfb,stroke:#333,stroke-width:1px;
    classDef domainLayer fill:#fbb,stroke:#333,stroke-width:1px;
    classDef dataLayer fill:#ddd,stroke:#333,stroke-width:2px;
    
    class PersonajesAPI,MisionesAPI,PersonajesMisionesAPI apiLayer;
    class PersonajeService,MisionService,ColaService serviceLayer;
    class PersonajeRepo,MisionRepo,PersonajeMisionRepo repoLayer;
    class Personaje,Mision,PersonajeMision,Cola,ColaBD domainLayer;
    class DB dataLayer;
```

El diagrama de componentes muestra la estructura a alto nivel del sistema, ilustrando cómo están organizados los diferentes módulos y sus dependencias entre sí. Podemos observar la clara separación en capas, donde cada componente tiene una responsabilidad bien definida y depende únicamente de los componentes de su misma capa o capas inferiores.
