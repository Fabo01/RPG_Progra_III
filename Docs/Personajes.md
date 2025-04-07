# Documentación de Personajes - Sistema RPG de Misiones

## 1. Introducción a los Personajes en el RPG

### 1.1 Concepto de Personaje

En nuestro sistema RPG, un Personaje representa la entidad principal controlada por el usuario. Cada personaje tiene:

- **Estadísticas básicas**: Nivel, experiencia, salud, maná, oro
- **Contadores de misiones**: Registro de misiones completadas y canceladas
- **Relaciones**: Con misiones y colas separadas de misiones principales y secundarias.

Los personajes son el núcleo del sistema, ya que son quienes realizan las misiones y progresan a lo largo del juego mediante la acumulación de experiencia, subida de niveles y obtención de recursos.

### 1.2 Estructura de Datos del Personaje

Los personajes se modelan como entidades persistentes en la base de datos y como objetos en la lógica de la aplicación:

```python
class Personaje(Base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False, default=1)
    experiencia = Column(Integer, nullable=False, default=0)
    salud = Column(Integer, nullable=False, default=100)
    mana = Column(Integer, nullable=False, default=100)
    oro = Column(Float, nullable=False, default=0.0)
    misiones_completadas = Column(Integer, nullable=False, default=0)
    misiones_canceladas = Column(Integer, nullable=False, default=0)
```

## 2. Patrones Implementados

### 2.1 Patrón Repositorio

El patrón Repositorio se utiliza para encapsular la lógica de acceso a datos, separándola del resto de la aplicación. Este patrón nos permite:

- **Abstraer la persistencia**: El resto de la aplicación no necesita saber cómo se almacenan los datos
- **Centralizar las consultas**: Todas las operaciones de base de datos están en un solo lugar
- **Facilitar pruebas**: Permite simular repositorios para testing sin acceder a la BD real

**Ejemplo de implementación**:

```python
class PersonajeRepositorio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def crear_personaje(self, personaje_data):
        nuevo_personaje = Personaje(**personaje_data)
        self.db_session.add(nuevo_personaje)
        self.db_session.commit()
        self.db_session.refresh(nuevo_personaje)
        return nuevo_personaje
    
    def obtener_personaje_por_id(self, personaje_id):
        personaje = self.db_session.query(Personaje).filter(Personaje.id == personaje_id).first()
        if not personaje:
            raise PersonajeNoEncontradoError(f"No se encontró el personaje con ID {personaje_id}")
        return personaje
```

### 2.2 Patrón Servicio

El patrón Servicio implementa la lógica de negocio, coordinando las acciones entre el repositorio y otros componentes. Sus beneficios son:

- **Separación de responsabilidades**: La lógica de negocio está separada del acceso a datos y la API
- **Reutilización**: Los servicios pueden ser usados por diferentes controladores o rutas
- **Orquestación**: Coordina operaciones complejas que involucran múltiples entidades

**Ejemplo de implementación**:

```python
class PersonajeServicio:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.personaje_repo = PersonajeRepositorio(db_session)
    
    def completar_mision(self, personaje_id, mision_id):
        # Buscar la relación personaje-misión
        personaje_mision = self.db_session.query(PersonajesMisiones).filter_by(
            personaje_id=personaje_id, mision_id=mision_id
        ).first()
        
        if not personaje_mision:
            raise ValueError(f"La misión {mision_id} no está asignada al personaje {personaje_id}")
        
        # Actualizar estado de la misión
        personaje_mision.estado = 'completada'
        personaje_mision.fecha_finalizacion = datetime.now()
        
        # Obtener personaje y misión
        personaje = self.personaje_repo.obtener_personaje_por_id(personaje_id)
        mision = personaje_mision.mision
        
        # Calcular y otorgar recompensas
        exp_ganada = mision.experiencia * (1 + mision.dificultad * 0.1)
        oro_ganado = mision.recompensa_oro * (1 + mision.dificultad * 0.1)
        
        personaje.ganar_experiencia(exp_ganada)
        personaje.ganar_oro(oro_ganado)
        personaje.misiones_completadas += 1
        
        self.db_session.commit()
        
        return {
            "personaje": personaje,
            "mision": mision,
            "experiencia_ganada": exp_ganada,
            "oro_ganado": oro_ganado,
            "nivel_actual": personaje.nivel
        }
```

### 2.3 Patrón DTO (Data Transfer Object)

Los DTOs son objetos que transportan datos entre procesos, especialmente útiles para definir la interfaz de la API:

- **Validación de datos**: Permiten definir reglas de validación en la entrada
- **Documentación**: Auto-documentan la API mostrando la estructura esperada
- **Seguridad**: Evitan la exposición de datos sensibles o innecesarios

**Ejemplo de implementación**:

```python
class PersonajeBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)

class PersonajeCreacion(PersonajeBase):
    pass

class PersonajeRespuesta(PersonajeBase):
    id: int
    nivel: int
    experiencia: int
    salud: int
    mana: int
    oro: float
    misiones_completadas: int
    misiones_canceladas: int
    
    class Config:
        orm_mode = True
```

### 2.4 Comportamiento de Dominio Rico

El modelo de Personaje incluye comportamientos propios, siguiendo el principio de "Tell, Don't Ask". Los objetos encapsulan tanto datos como comportamiento:

```python
def ganar_experiencia(self, cantidad):
    """Añade experiencia al personaje y sube de nivel si corresponde"""
    self.experiencia += cantidad
    exp_necesaria = self.nivel * 100
    if self.experiencia >= exp_necesaria:
        self.subir_nivel()
        self.experiencia -= exp_necesaria

def subir_nivel(self):
    """Sube de nivel al personaje y ajusta sus estadísticas"""
    self.nivel += 1
    self.salud += 10
    self.mana += 5
```

## 3. Flujo de Operaciones con Personajes

### 3.1 Ciclo de Vida de un Personaje

1. **Creación**: Un personaje se crea con estadísticas base y sin misiones
2. **Asignación de misiones**: Se le asignan misiones que se añaden a sus colas
3. **Completar/Cancelar misiones**: El personaje completa o cancela misiones, afectando sus estadísticas
4. **Progresión**: Al completar misiones, gana experiencia y oro, pudiendo subir de nivel
5. **Consulta**: Se puede consultar el estado del personaje y sus misiones en cualquier momento

### 3.2 Integración con el Sistema de Colas

Cada personaje tiene dos colas de misiones:

```python
# Obtener cola principal del personaje con ID 1
cola_servicio = ColaServicio(db_session)
cola_principal = cola_servicio.obtener_cola_personaje(personaje_id=1, tipo_cola='principal')

# Obtener cola secundaria del personaje con ID 1
cola_secundaria = cola_servicio.obtener_cola_personaje(personaje_id=1, tipo_cola='secundaria')
```

## 4. Ejemplos de Uso

### 4.1 Crear un nuevo personaje

```python
# A través de la API REST:
# POST /personajes
payload = {
    "nombre": "Gandalf"
}

# Respuesta
{
    "id": 1,
    "nombre": "Gandalf",
    "nivel": 1,
    "experiencia": 0,
    "salud": 100,
    "mana": 100,
    "oro": 0.0,
    "misiones_completadas": 0,
    "misiones_canceladas": 0
}
```

### 4.2 Asignar y completar una misión

```python
# Asignar misión
# POST /personajes-misiones/asignar/5/a/1
# Respuesta: información sobre la asignación

# Completar misión
# POST /personajes-misiones/completar/5/personaje/1
# Respuesta
{
    "personaje": {
        "id": 1,
        "nombre": "Gandalf",
        "nivel": 1,
        "experiencia": 50,
        "salud": 100,
        "mana": 100,
        "oro": 25.5,
        "misiones_completadas": 1,
        "misiones_canceladas": 0
    },
    "mision": {
        "id": 5,
        "nombre": "Explorar la mina",
        "tipo": "exploracion",
        "dificultad": 3,
        ...
    },
    "tipo_mision": "exploracion",
    "multiplicador_tipo": 1.1,
    "experiencia_base": 45.45,
    "experiencia_ganada": 50,
    "oro_base": 23.18,
    "oro_ganado": 25.5,
    "nivel_actual": 1
}
```

### 4.3 Consultar el ranking de personajes

```python
# GET /personajes/ranking
[
    {
        "id": 3,
        "nombre": "Aragorn",
        "nivel": 10,
        "misiones_completadas": 57
    },
    {
        "id": 1,
        "nombre": "Gandalf",
        "nivel": 8,
        "misiones_completadas": 42
    },
    ...
]
```

## 5. Manejo de Errores

El sistema implementa excepciones personalizadas para un manejo coherente de errores:

```python
# Cuando se busca un personaje que no existe
try:
    personaje = personaje_servicio.obtener_personaje(999)
except PersonajeNoEncontradoError as e:
    # Manejar el error (por ejemplo, devolver 404 en la API)
    print(e)  # "No se encontró el personaje con ID 999"
```

## 6. Conclusión sobre Personajes en el RPG

Los Personajes constituyen el elemento central del sistema RPG, actuando como protagonistas que avanzan en el juego a través de la realización de misiones. La implementación sigue varios patrones y principios importantes:

1. **Separación de responsabilidades**: Cada componente (modelo, repositorio, servicio, DTOs) tiene una responsabilidad clara y bien definida, siguiendo el principio de responsabilidad única de SOLID.

2. **Encapsulamiento de lógica de negocio**: Comportamientos como ganar experiencia y subir de nivel están encapsulados en el modelo de dominio, garantizando la coherencia del estado interno.

3. **Persistencia transparente**: La capa de repositorio aísla al dominio de los detalles de persistencia, permitiendo centrarse en la lógica de negocio.

4. **Interfaz clara y validada**: Los DTOs definen contratos explícitos para la comunicación con el exterior, con validaciones incorporadas.

5. **Cohesión entre sistemas**: La integración con el sistema de colas permite una gestión ordenada de las misiones por personaje.

La arquitectura implementada permite que los personajes evolucionen de manera coherente en función de sus logros, manteniendo siempre la integridad de los datos y ofreciendo una interfaz clara para interactuar con ellos. Esta base sólida facilitará futuras extensiones como la implementación de clases, razas, inventarios y habilidades especiales.

La combinación de los principios arquitectónicos aplicados garantiza que el sistema sea mantenible, escalable y adaptable a nuevos requisitos a medida que el juego evolucione.
