# Documentación TDA_Cola - Sistema RPG de Misiones

## 1. Introducción a TDA Cola

### 1.1 ¿Qué es un TDA?

Un Tipo de Dato Abstracto (TDA) es un modelo matemático que define:
- Una colección de datos
- Un conjunto de operaciones permitidas sobre esos datos
- Las propiedades que deben cumplir esas operaciones

Los TDAs son fundamentales en programación porque:
- **Encapsulamiento**: Separan la interfaz (qué hace) de la implementación (cómo lo hace)
- **Modularidad**: Permiten construir componentes reutilizables e independientes
- **Abstracción**: Facilitan pensar en términos de operaciones de alto nivel
- **Ocultamiento de información**: Los detalles internos quedan protegidos

### 1.2 ¿Qué es un TDA Cola?

Una Cola es un TDA que implementa una estructura secuencial siguiendo el principio FIFO (First In, First Out), donde el primer elemento añadido será el primero en ser retirado. En las colas, las operaciones principales ocurren en ambos extremos: se añaden elementos al final y se eliminan desde el principio.

### 1.3 Operaciones fundamentales

- **enqueue**: Añade un elemento al final de la cola
- **dequeue**: Elimina y retorna el primer elemento de la cola
- **first** (o peek): Consulta el primer elemento sin eliminarlo
- **is_empty**: Verifica si la cola está vacía
- **size**: Obtiene el número de elementos en la cola

## 2. Implementación en el Sistema RPG

### 2.1 Estructura de la implementación

En nuestro sistema RPG, implementamos el TDA Cola siguiendo estos principios fundamentales:

**Principios de la implementación**:
1. **Separación de la interfaz y la implementación**: Ofrecemos métodos estándar de cola sin exponer detalles internos.
2. **Comportamiento FIFO estricto**: Garantizamos que las misiones se procesan en el orden exacto en que fueron aceptadas.
3. **Persistencia y recuperabilidad**: Las colas pueden reconstructuirse desde la base de datos, manteniendo su estado.

**Detalles técnicos de la implementación**:
La clase `TDA_Cola` utiliza una lista Python como estructura de almacenamiento interna:
- El método `enqueue()` utiliza `append()` para añadir al final (O(1)) 
- El método `dequeue()` utiliza `pop(0)` para eliminar desde el principio (O(n))
- El acceso al primer elemento se realiza mediante indexación directa `[0]` (O(1))

```python
class TDA_Cola:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        # Añade al final de la lista (O(1) amortizado)
        self.items.append(item)
    
    def dequeue(self):
        # Comprueba si está vacía
        if self.is_empty():
            return None
        # Elimina y devuelve el primer elemento (O(n))
        return self.items.pop(0)
    
    def first(self):
        # Comprueba si está vacía
        if self.is_empty():
            return None
        # Devuelve el primer elemento sin eliminarlo (O(1))
        return self.items[0]
    
    def is_empty(self):
        # Verifica si la cola está vacía (O(1))
        return len(self.items) == 0
    
    def size(self):
        # Devuelve el tamaño de la cola (O(1))
        return len(self.items)
```

**Implicaciones de rendimiento**:
- Para colas pequeñas (típicas en un sistema de misiones por personaje), el rendimiento es adecuado.
- Si las colas crecieran significativamente, podríamos optimizar usando `collections.deque`, que ofrece operaciones O(1) en ambos extremos.

### 2.2 Persistencia de Colas

Para mantener las colas entre sesiones, utilizamos una tabla en la base de datos:

```python
class ColaFIFO(Base):
    __tablename__ = 'colas_fifo'
    id = Column(Integer, primary_key=True)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), nullable=False)
    tipo_cola = Column(String, nullable=False)  # 'principal' o 'secundaria'
    misiones_orden = Column(JSON, nullable=False, default=[])
    
    personaje = relationship("Personaje", back_populates="colas")
```

## 3. Funcionamiento del Sistema de Colas en el RPG

### 3.1 Colas por Personaje

Cada personaje tiene dos colas independientes:
- **Cola Principal**: Para misiones de la categoría "principal"
- **Cola Secundaria**: Para misiones de la categoría "secundaria"

Esto permite que cada personaje gestione misiones principales y secundarias por separado. Las colas son específicas para cada personaje, garantizando que las misiones de un personaje no interfieran con las de otros.

### 3.2 Flujo de Trabajo

1. **Asignación de Misión**: Cuando una misión se asigna a un personaje mediante el endpoint `/personajes-misiones/asignar/{mision_id}/a/{personaje_id}`, el sistema:
   - Registra la relación en la tabla `misiones_personajes`
   - Determina la categoría de la misión (principal o secundaria)
   - Encola la misión en la cola correspondiente del personaje

2. **Encolamiento**: El proceso de encolamiento está centralizado en `ColaServicio.encolar_mision()`:
   - Obtiene la cola TDA del personaje
   - Añade la misión al final de la cola
   - Guarda el estado actualizado de la cola en la base de datos

3. **Gestión de Colas**: El endpoint `/personajes-misiones/personaje/{personaje_id}/cola/{tipo_cola}` permite consultar:
   - El estado de cada cola
   - Si la cola está vacía
   - El tamaño de la cola
   - La próxima misión a completar

4. **Completar Misión**: Al completar una misión mediante `/personajes-misiones/completar/{mision_id}/personaje/{personaje_id}`:
   - Se desencola automáticamente de la cola correspondiente
   - Se actualiza el estado a "completada" en la tabla `misiones_personajes`
   - Se calculan recompensas basadas en tipo y dificultad
   - El personaje recibe experiencia y oro según multiplicadores

5. **Cancelar Misión**: Al cancelar una misión mediante `/personajes-misiones/cancelar/{mision_id}/personaje/{personaje_id}`:
   - Se desencola automáticamente de la cola correspondiente
   - Se actualiza el estado a "cancelada" en la tabla `misiones_personajes`
   - Se incrementa el contador de misiones canceladas del personaje

### 3.3 Conversión entre BD y TDA_Cola

El servicio `ColaServicio` gestiona la conversión entre la persistencia y los objetos en memoria:

1. **Obtención de cola desde BD**: 
   - El método `obtener_cola_personaje()` consulta la tabla `colas_fifo`
   - Si no existe la cola para el personaje, la crea
   - Lee los IDs de misiones ordenados del campo JSON `misiones_orden`
   - Consulta las relaciones `PersonajesMisiones` correspondientes
   - Crea un objeto `TDA_Cola` y lo rellena en el orden correcto

2. **Guardar cola en BD**:
   - El método `guardar_cola_personaje()` toma un objeto `TDA_Cola`
   - Extrae los IDs de misiones en orden
   - Actualiza el campo JSON `misiones_orden` en la tabla `colas_fifo`

3. **Operaciones de cola**:
   - Para operaciones como `encolar_mision()` y `desencolar_mision()`, el servicio:
     - Primero obtiene la cola desde la BD
     - Realiza la operación en memoria
     - Guarda el estado actualizado en la BD

Este proceso garantiza la consistencia entre el estado en memoria y el estado persistente.

## 4. Ejemplos de Uso

### 4.1 Encolar una misión nueva

```python
# Asignar y encolar una misión de tipo combate a un personaje
# POST /personajes-misiones/asignar/5/a/1
# Respuesta
{
    "mision_id": 5,
    "personaje_id": 1,
    "estado": "pendiente",
    "fecha_asignacion": "2023-10-20T15:30:00",
    "fecha_finalizacion": null
}

# Internamente, el sistema ejecuta:
servicio = MisionServicio(db)
mision = servicio.obtener_mision_por_id(5)  # Comprueba que la misión existe
personaje_mision = servicio.personaje_mision_repo.asignar_mision(1, 5)
es_principal = mision.categoria == 'principal'
servicio.cola_servicio.encolar_mision(1, 5, es_principal)
```

### 4.2 Completar la próxima misión

```python
# Completar una misión y recibir recompensas ajustadas por tipo
# POST /personajes-misiones/completar/5/personaje/1
# Respuesta
{
    "personaje": {
        "id": 1,
        "nombre": "Gandalf",
        "nivel": 1,
        "experiencia": 75,  # Aumentada por el multiplicador de tipo
        "salud": 100,
        "mana": 100,
        "oro": 37.5,  # Aumentado por el multiplicador de tipo
        "misiones_completadas": 1,
        "misiones_canceladas": 0
    },
    "mision": {
        "id": 5,
        "nombre": "Eliminar enemigos",
        "tipo": "combate",  # Tipo de misión con multiplicador 1.5x
        "dificultad": 3,
        ...
    },
    "tipo_mision": "combate",
    "multiplicador_tipo": 1.5,
    "experiencia_base": 50,
    "experiencia_ganada": 75,
    "oro_base": 25,
    "oro_ganado": 37.5,
    "nivel_actual": 1
}
```

### 4.3 Consultar la cola de misiones de un personaje

```python
# Ver el estado de la cola secundaria de un personaje
# GET /personajes-misiones/personaje/1/cola/secundaria
# Respuesta
{
    "personaje_id": 1,
    "tipo_cola": "secundaria",
    "esta_vacia": false,
    "tamano": 2,
    "proxima_mision": {
        "id": 8,
        "nombre": "Recolectar hierbas",
        "tipo": "recoleccion",
        "categoria": "secundaria",
        ...
    }
}
```

## 5. Conclusión

### 5.1 Beneficios de la implementación de Colas en el RPG

La implementación del TDA Cola para el sistema de misiones proporciona múltiples ventajas:

1. **Organización estructurada de misiones**: Los personajes pueden gestionar sus misiones de forma ordenada y predecible, siguiendo un flujo de trabajo coherente.

2. **Separación de responsabilidades**: Cada personaje tiene dos colas independientes (principal y secundaria), permitiendo priorización natural entre tipos de misiones.

3. **Independencia entre personajes**: Las colas son individuales por personaje, lo que permite que cada uno tenga su propio progreso sin afectar a otros.

4. **Persistencia entre sesiones**: Las colas se almacenan en la base de datos, preservando el estado del juego entre sesiones.

5. **Abstracción del orden de misiones**: El sistema encapsula la lógica de ordenamiento, facilitando la programación de otros componentes.

### 5.2 Características técnicas y de diseño

La implementación técnica de las colas proporciona:

1. **Bajo acoplamiento**: La separación entre TDA_Cola y ColaFIFO permite modificar la implementación subyacente sin afectar la lógica de negocio.

2. **Alta cohesión**: Cada componente tiene una responsabilidad clara y bien definida.

3. **Persistencia transparente**: El servicio maneja automáticamente la conversión entre objetos en memoria y registros en la base de datos.

4. **Manejo de errores robusto**: Se incluye gestión de excepciones específicas como ColaVaciaError.

### 5.3 Escalabilidad y extensibilidad

El diseño actual es extensible para futuros desarrollos como:

1. **Implementación de colas de prioridad**: Permitiría organizar misiones por importancia dentro de cada categoría.

2. **Sistemas de dependencias**: Podría expandirse para implementar prerrequisitos entre misiones.

3. **Colas con tiempo limitado**: Se podrían implementar misiones con fecha de expiración automática.

En resumen, la implementación del TDA Cola provee una base sólida para el sistema de misiones del RPG, combinando principios teóricos de estructuras de datos con necesidades prácticas de un juego de rol, todo bajo una arquitectura extensible y mantenible.

