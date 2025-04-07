# Documentación de Misiones - Sistema RPG

## 1. Introducción a las Misiones en el RPG

### 1.1 Concepto de Misión

En nuestro sistema RPG, una Misión representa un objetivo o tarea que los personajes pueden completar para obtener recompensas. Cada misión tiene:

- **Características básicas**: Nombre, descripción, tipo, categoría, dificultad
- **Temporalidad**: Fecha de creación, fecha límite (opcional)
- **Recompensas**: Experiencia y oro que se otorgan al completar la misión
- **Estado**: Pendiente, completada o cancelada
- **Diversidad**: Diferentes tipos de misiones con distintos multiplicadores de recompensa

Las misiones son el principal mecanismo de progresión en el juego, permitiendo a los personajes ganar experiencia, subir de nivel y obtener recursos.

### 1.2 Estructura de Datos de la Misión

Las misiones se modelan como entidades persistentes en la base de datos:

```python
class Mision(Base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)
    # Tipos de misión con diferente dificultad y recompensa
    # sigilo=combate > rescate > escolta > exploracion > recoleccion
    tipo = Column(
        Enum('sigilo', 'combate', 'rescate', 'escolta', 'exploracion', 'recoleccion'), 
        nullable=False,
        default='combate'
    )
    categoria = Column(
        Enum('principal', 'secundaria'), 
        nullable=False, 
        default='secundaria'
    )
    estado = Column(
        Enum('pendiente', 'completada', 'cancelada'), 
        nullable=False, 
        default='pendiente'
    )
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False) 
    fecha_limite = Column(DateTime, nullable=True)
    dificultad = Column(Integer, nullable=False)  # 1 a 10
    experiencia = Column(Float, nullable=False)  # experiencia base de la misión
    recompensa_oro = Column(Float, nullable=False)  # Recompensa en oro base de la misión

    personajes = relationship("PersonajesMisiones", back_populates="mision")  # Relación muchos a muchos con personajes
```

### 1.3 Tipos de Misiones y Multiplicadores

El sistema implementa varios tipos de misiones, cada uno con su propio multiplicador de recompensa que refleja la dificultad inherente al tipo:

| Tipo de Misión | Multiplicador | Descripción |
|----------------|---------------|-------------|
| Sigilo         | 1.5           | Misiones que requieren sigilo y estrategia |
| Combate        | 1.5           | Misiones de combate contra enemigos |
| Rescate        | 1.3           | Misiones para rescatar personajes o recuperar objetos |
| Escolta        | 1.2           | Misiones para escoltar a un personaje o proteger una caravana |
| Exploración    | 1.1           | Misiones para explorar áreas o mapas |
| Recolección    | 1.0           | Misiones para recolectar recursos o materiales |

Estos multiplicadores afectan directamente las recompensas finales, aumentando tanto la experiencia como el oro obtenidos.

## 2. Patrones Implementados

### 2.1 Patrón Repositorio

El patrón Repositorio se utiliza para encapsular toda la lógica de acceso a datos relacionada con las misiones:

```python
class MisionRepositorio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def crear_mision(self, mision_data):
        """Crea una nueva misión en la base de datos"""
        if 'fecha_creacion' not in mision_data:
            mision_data['fecha_creacion'] = datetime.now()
            
        nueva_mision = Mision(**mision_data)
        self.db_session.add(nueva_mision)
        self.db_session.commit()
        self.db_session.refresh(nueva_mision)
        return nueva_mision
    
    def obtener_mision_por_id(self, mision_id):
        """Obtiene una misión por su ID"""
        mision = self.db_session.query(Mision).filter(Mision.id == mision_id).first()
        if not mision:
            raise MisionNoEncontradaError(f"No se encontró la misión con ID {mision_id}")
        return mision
```

Este patrón nos permite:

- Centralizar todas las consultas relacionadas con misiones
- Abstraer la complejidad del acceso a datos
- Facilitar la modificación de la lógica de persistencia sin afectar a los servicios

### 2.2 Patrón Servicio

El patrón Servicio implementa la lógica de negocio relacionada con las misiones:

```python
class MisionServicio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.mision_repo = MisionRepositorio(db_session)
        self.personaje_mision_repo = PersonajeMisionRepositorio(db_session)
        self.cola_servicio = ColaServicio(db_session)
    
    def asignar_mision_a_personaje(self, mision_id, personaje_id):
        """Asigna una misión a un personaje"""
        # Verificar que exista la misión
        mision = self.mision_repo.obtener_mision_por_id(mision_id)
        
        # Crear la relación personaje-misión
        personaje_mision = self.personaje_mision_repo.asignar_mision(personaje_id, mision_id)
        
        # Encolar la misión según su categoría
        es_principal = mision.categoria == 'principal'
        self.cola_servicio.encolar_mision(personaje_id, mision_id, es_principal)
        
        return personaje_mision
```

Este patrón:

- Orquesta la interacción entre diferentes componentes (repositorios, colas)
- Implementa reglas de negocio complejas
- Centraliza la lógica de misiones en un solo lugar

### 2.3 Patrón DTO (Data Transfer Object)

Los DTOs definen la estructura de datos para la comunicación en la API:

```python
class MisionBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=10)
    tipo: str = Field(..., description=f"Tipo de misión: {', '.join(TIPOS_MISION)}")
    categoria: str = Field(..., regex='^(principal|secundaria)$')
    dificultad: int = Field(..., ge=1, le=10)
    experiencia: float = Field(..., gt=0)
    recompensa_oro: float = Field(..., ge=0)
    
    @validator('tipo')
    def tipo_valido(cls, v):
        if v not in TIPOS_MISION:
            raise ValueError(f'El tipo debe ser uno de: {", ".join(TIPOS_MISION)}')
        return v
```

### 2.4 Patrón de Relación Muchos a Muchos

La relación entre Personajes y Misiones se modela como una relación muchos a muchos con atributos adicionales:

```python
class PersonajesMisiones(Base): 
    __tablename__ = 'misiones_personajes'
    mision_id = Column(Integer, ForeignKey('misiones.id'), primary_key=True)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), primary_key=True)
    estado = Column(Enum('pendiente', 'completada', 'cancelada'), default='pendiente')
    fecha_asignacion = Column(DateTime, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=True)

    personaje = relationship('Personaje', back_populates='misiones')
    mision = relationship('Mision', back_populates='personajes')
```

Este patrón permite:

- Realizar un seguimiento del estado de cada misión por personaje
- Registrar información temporal (cuándo se asignó y completó)
- Mantener la independencia entre entidades Personaje y Misión

## 3. Flujo de Operaciones con Misiones

### 3.1 Ciclo de Vida de una Misión

1. **Creación**: Una misión se crea con sus características básicas y recompensas
2. **Asignación**: La misión se asigna a uno o varios personajes
3. **Encolamiento**: La misión se añade a la cola principal o secundaria de cada personaje
4. **Realización**: Los personajes completan (o cancelan) las misiones
5. **Recompensa**: Al completar una misión, se calculan y otorgan las recompensas según tipo y dificultad

### 3.2 Integración con el Sistema de Personajes

Las misiones afectan directamente el progreso de los personajes:

1. **Asignación**: Se crea un vínculo `PersonajesMisiones` que registra esta relación
2. **Seguimiento**: El estado de cada misión se mantiene de forma independiente para cada personaje
3. **Impacto**: Al completar misiones, los personajes:
   - Ganan experiencia (ajustada por tipo y dificultad)
   - Obtienen oro (ajustado por tipo y dificultad)
   - Incrementan su contador de misiones completadas
   - Pueden subir de nivel si alcanzan suficiente experiencia

### 3.3 Integración con el Sistema de Colas

Las misiones interactúan directamente con las colas:

```python
def asignar_mision_a_personaje(self, mision_id, personaje_id):
    # Verificar que exista la misión
    mision = self.mision_repo.obtener_mision_por_id(mision_id)
    
    # Crear la relación personaje-misión
    personaje_mision = self.personaje_mision_repo.asignar_mision(personaje_id, mision_id)
    
    # Encolar la misión según su categoría
    es_principal = mision.categoria == 'principal'
    self.cola_servicio.encolar_mision(personaje_id, mision_id, es_principal)
    
    return personaje_mision
```

1. Las misiones principales se encolan en la cola principal
2. Las misiones secundarias se encolan en la cola secundaria
3. Al completar o cancelar una misión, se desencola automáticamente

## 4. Ejemplos de Uso

### 4.1 Crear una nueva misión

```python
# POST /misiones
payload = {
    "nombre": "El bosque encantado",
    "descripcion": "Explorar el bosque en busca de criaturas mágicas",
    "tipo": "exploracion",
    "categoria": "secundaria",
    "dificultad": 4,
    "experiencia": 100,
    "recompensa_oro": 50
}

# Respuesta
{
    "id": 5,
    "nombre": "El bosque encantado",
    "descripcion": "Explorar el bosque en busca de criaturas mágicas",
    "tipo": "exploracion",
    "categoria": "secundaria",
    "dificultad": 4,
    "experiencia": 100,
    "recompensa_oro": 50,
    "estado": "pendiente",
    "fecha_creacion": "2023-10-15T14:30:25",
    "fecha_limite": null
}
```

### 4.2 Asignar una misión a un personaje

```python
# POST /personajes-misiones/asignar/5/a/1
# Respuesta
{
    "mision_id": 5,
    "personaje_id": 1,
    "estado": "pendiente",
    "fecha_asignacion": "2023-10-15T14:35:10",
    "fecha_finalizacion": null
}
```

### 4.3 Obtener misiones por tipo

```python
# GET /misiones?tipo=combate
[
    {
        "id": 3,
        "nombre": "La torre oscura",
        "descripcion": "Derrotar al nigromante en la torre",
        "tipo": "combate",
        "categoria": "principal",
        "estado": "pendiente",
        "dificultad": 8,
        ...
    },
    {
        "id": 7,
        "nombre": "Bandidos del camino",
        "descripcion": "Eliminar a los bandidos que acechan el camino real",
        "tipo": "combate",
        "categoria": "secundaria",
        "estado": "pendiente",
        "dificultad": 5,
        ...
    }
]
```

### 4.4 Completar una misión y recibir recompensas

```python
# POST /personajes-misiones/completar/5/personaje/1
# Respuesta
{
    "personaje": {
        "id": 1,
        "nombre": "Gandalf",
        "nivel": 1,
        "experiencia": 121,  # Experiencia base × dificultad × tipo
        "salud": 100,
        "mana": 100,
        "oro": 60.5,  # Oro base × dificultad × tipo
        "misiones_completadas": 1,
        "misiones_canceladas": 0
    },
    "mision": {
        "id": 5,
        "nombre": "El bosque encantado",
        "tipo": "exploracion",
        "dificultad": 4,
        ...
    },
    "tipo_mision": "exploracion",
    "multiplicador_tipo": 1.1,  # Multiplicador específico para misiones de exploración
    "experiencia_base": 100,
    "experiencia_ganada": 121,  # 100 × (1 + 0.1 × 4) × 1.1
    "oro_base": 50,
    "oro_ganado": 60.5,  # 50 × (1 + 0.1 × 4) × 1.1
    "nivel_actual": 1
}
```

## 5. Manejo de Errores

El sistema implementa excepciones específicas para manejar errores relacionados con misiones:

```python
try:
    # Intentar obtener una misión que no existe
    mision = mision_servicio.obtener_mision(999)
except MisionNoEncontradaError as e:
    # Manejar el error
    print(e)  # "No se encontró la misión con ID 999"
```

Otros errores comunes incluyen:

```python
# Intentar completar una misión que no está asignada al personaje
try:
    resultado = mision_servicio.completar_mision_personaje(999, 1)
except ValueError as e:
    print(e)  # "La misión 999 no está asignada al personaje 1"

# Intentar desencolar una misión cuando la cola está vacía
try:
    cola_servicio.desencolar_mision(1, True)  # cola principal
except ColaVaciaError as e:
    print(e)  # "La cola principal del personaje 1 está vacía"
```

## 6. Conclusión sobre Misiones en el RPG

Las Misiones constituyen el motor principal de progresión en nuestro sistema RPG, proporcionando objetivos claros y recompensas significativas a los jugadores. Nuestra implementación destaca por:

1. **Sistema de tipos diverso**: Diferentes tipos de misiones con distintos multiplicadores de recompensa añaden variedad y estrategia a la jugabilidad.

2. **Integración robusta**: Las misiones están estrechamente integradas con los sistemas de personajes y colas, creando un flujo coherente desde la asignación hasta la recompensa.

3. **Flexibilidad en recompensas**: El cálculo de recompensas considera múltiples factores (experiencia base, dificultad, tipo de misión), creando un sistema equilibrado y justo.

4. **Arquitectura sólida**: El uso de patrones como Repositorio, Servicio y DTO garantiza la mantenibilidad y extensibilidad del sistema.

5. **Asociación independiente**: La tabla intermedia `PersonajesMisiones` permite que cada personaje mantenga su propio estado para cada misión.

Este sistema de misiones proporciona una base robusta sobre la que se pueden construir características adicionales como cadenas de misiones, misiones con tiempo limitado o misiones especiales de eventos. La implementación actual es escalable y puede adaptarse fácilmente a nuevos requisitos a medida que el juego evoluciona.
