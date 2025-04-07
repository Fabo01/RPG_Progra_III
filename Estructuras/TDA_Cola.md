# Documentación TDA_Cola - Sistema RPG de Misiones

## 1. Introducción a TDA Cola

### 1.1 ¿Qué es un TDA Cola?

Un Tipo de Dato Abstracto (TDA) Cola, o Queue en inglés, es una estructura de datos que sigue el principio FIFO (First In, First Out), es decir, el primer elemento que entra es el primero que sale. Podemos imaginarlo como una cola de personas esperando en una tienda: la primera persona que llega es la primera en ser atendida.

### 1.2 Operaciones fundamentales

- **enqueue**: Añade un elemento al final de la cola
- **dequeue**: Elimina y retorna el primer elemento de la cola
- **first** (o peek): Consulta el primer elemento sin eliminarlo
- **is_empty**: Verifica si la cola está vacía
- **size**: Obtiene el número de elementos en la cola

## 2. Implementación en el Sistema RPG

### 2.1 Estructura de la implementación

En nuestro sistema RPG, la implementación de `TDA_Cola` se realiza mediante una lista de Python:

```python
class TDA_Cola:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def first(self):
        if self.is_empty():
            return None
        return self.items[0]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

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

Esto permite que cada personaje gestione sus misiones de forma ordenada según su importancia.

### 3.2 Flujo de Trabajo

1. **Asignación de Misión**: Cuando una misión se asigna a un personaje, se registra en la tabla `misiones_personajes`.
2. **Encolamiento**: La misión se añade a la cola correspondiente (principal o secundaria) del personaje.
3. **Gestión de Colas**: El personaje puede ver qué misión debe completar primero (la que está al inicio de la cola).
4. **Completar Misión**: Al completar una misión, se desencola y se actualiza su estado en `misiones_personajes`.

### 3.3 Conversión entre BD y TDA_Cola

Para trabajar con las colas, el sistema:
1. Lee el orden de misiones desde `ColaFIFO` (tabla BD)
2. Construye un objeto `TDA_Cola` con esas misiones
3. Realiza operaciones sobre la cola en memoria
4. Guarda el nuevo estado en la base de datos

## 4. Ejemplos de Uso

### 4.1 Encolar una misión nueva

```python
# Asignar y encolar una misión secundaria al personaje con ID 1
cola_servicio = ColaServicio(db_session)
resultado = cola_servicio.encolar_mision(personaje_id=1, mision_id=5, es_principal=False)
```

### 4.2 Completar la próxima misión

```python
# Completar la próxima misión principal del personaje con ID 1
cola_servicio = ColaServicio(db_session)
mision_completada = cola_servicio.desencolar_mision(personaje_id=1, es_principal=True)

# Actualizar estado y dar recompensas
mision_completada.estado = 'completada'
mision_completada.fecha_finalizacion = datetime.now()
```

### 4.3 Consultar la próxima misión

```python
# Ver cuál es la próxima misión secundaria sin completarla
cola_servicio = ColaServicio(db_session)
proxima_mision = cola_servicio.obtener_primera_mision(personaje_id=1, es_principal=False)

if proxima_mision:
    print(f"Tu próxima misión es: {proxima_mision.mision.nombre}")
else:
    print("No tienes misiones pendientes")
```

## 5. Diagramas

### 5.1 Estructura de Colas por Personaje

