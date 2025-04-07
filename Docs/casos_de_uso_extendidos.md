# Casos de Uso Extendidos - Sistema RPG de Misiones

Este documento proporciona una descripción detallada de todos los casos de uso del sistema RPG, incluyendo flujos principales, alternativos, precondiciones y postcondiciones.

**Total de Casos de Uso Extendidos: 27**

## Índice
1. [Gestión de Personajes](#1-gestión-de-personajes) *(6 casos de uso)*
2. [Gestión de Misiones](#2-gestión-de-misiones) *(8 casos de uso)*
3. [Gestión de Asignación y Progreso](#3-gestión-de-asignación-y-progreso) *(6 casos de uso)*
4. [Gestión de Colas de Misiones](#4-gestión-de-colas-de-misiones) *(2 casos de uso)*
5. [Consultas y Reportes](#5-consultas-y-reportes) *(3 casos de uso)*
6. [Administración del Sistema](#6-administración-del-sistema) *(2 casos de uso)*

---

## 1. Gestión de Personajes

### CU-P01: Crear Personaje

**Actores**: Usuario

**Descripción**: Permite al usuario crear un nuevo personaje con estadísticas iniciales predefinidas.

**Precondiciones**: 
- El usuario debe estar autenticado en el sistema (si aplica).

**Flujo Principal**:
1. El usuario solicita crear un nuevo personaje.
2. El sistema muestra un formulario para ingresar los datos del personaje.
3. El usuario introduce el nombre del personaje.
4. El sistema valida que el nombre cumpla con los requisitos (3-50 caracteres).
5. El sistema crea el personaje con valores predeterminados:
   - Nivel: 1
   - Experiencia: 0
   - Salud: 100
   - Maná: 100
   - Oro: 0.0
   - Misiones completadas: 0
   - Misiones canceladas: 0
6. El sistema almacena el personaje en la base de datos.
7. El sistema devuelve los datos del personaje creado, incluyendo su ID único.

**Flujos Alternativos**:
- **Nombre inválido**: Si el nombre no cumple con los requisitos, el sistema muestra un mensaje de error y solicita un nuevo nombre.

**Postcondiciones**:
- Se crea un nuevo personaje en el sistema.
- El personaje está listo para ser asignado a misiones.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Alta - Es el punto de entrada para nuevos usuarios.

---

### CU-P02: Obtener Personaje

**Actores**: Usuario

**Descripción**: Permite consultar la información detallada de un personaje específico.

**Precondiciones**: 
- El personaje debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver los detalles de un personaje específico proporcionando su ID.
2. El sistema busca el personaje en la base de datos.
3. El sistema recopila toda la información del personaje: estadísticas básicas, nivel, experiencia, oro, contador de misiones.
4. El sistema muestra todos los detalles del personaje.

**Flujos Alternativos**:
- **Personaje no encontrado**: Si no existe un personaje con el ID proporcionado, el sistema devuelve un mensaje de error 404.

**Postcondiciones**:
- Se muestran los datos actualizados del personaje.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Alta - Los usuarios consultan frecuentemente el estado de sus personajes.

### CU-P03: Listar Personajes

**Actores**: Usuario, Administrador

**Descripción**: Permite obtener una lista paginada de todos los personajes registrados.

**Precondiciones**: 
- Ninguna específica.

**Flujo Principal**:
1. El usuario solicita ver la lista de personajes.
2. El usuario puede especificar parámetros de paginación opcionales (skip y limit).
3. El sistema recupera los personajes de la base de datos según los parámetros de paginación.
4. El sistema devuelve la lista de personajes con sus datos básicos.

**Flujos Alternativos**:
- **Sin personajes**: Si no hay personajes registrados, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de personajes.

**Excepciones**:
- Parámetros de paginación inválidos: El sistema utiliza valores predeterminados (skip=0, limit=100).

**Frecuencia de uso**: Media - Principalmente por administradores o en pantallas de clasificación.

### CU-P04: Actualizar Personaje

**Actores**: Usuario

**Descripción**: Permite modificar los atributos de un personaje existente.

**Precondiciones**: 
- El personaje debe existir en el sistema.
- El usuario debe tener permisos para modificar el personaje.

**Flujo Principal**:
1. El usuario solicita actualizar un personaje específico por su ID.
2. El sistema verifica que el personaje existe.
3. El usuario proporciona los datos que desea actualizar (nombre en la implementación actual).
4. El sistema valida los datos proporcionados.
5. El sistema actualiza la información del personaje en la base de datos.
6. El sistema devuelve los datos actualizados del personaje.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Datos inválidos**: El sistema muestra un mensaje de error de validación.

**Postcondiciones**:
- La información del personaje se actualiza en el sistema.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Baja - Los atributos básicos de los personajes no se modifican frecuentemente.

### CU-P05: Eliminar Personaje

**Actores**: Usuario, Administrador

**Descripción**: Permite eliminar permanentemente un personaje con todos sus datos asociados.

**Precondiciones**: 
- El personaje debe existir en el sistema.
- El usuario debe tener permisos para eliminar el personaje.

**Flujo Principal**:
1. El usuario solicita eliminar un personaje específico por su ID.
2. El sistema verifica que el personaje existe.
3. El sistema elimina el personaje de la base de datos, incluyendo todas sus relaciones (misiones asignadas y colas).
4. El sistema confirma la eliminación del personaje.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.

**Postcondiciones**:
- El personaje y todos sus datos relacionados se eliminan permanentemente del sistema.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Muy baja - La eliminación de personajes es una operación poco común.

### CU-P06: Consultar Ranking de Personajes

**Actores**: Usuario

**Descripción**: Permite ver una lista de personajes ordenados por nivel y experiencia.

**Precondiciones**: 
- Deben existir personajes en el sistema.

**Flujo Principal**:
1. El usuario solicita ver el ranking de personajes.
2. El usuario puede especificar un límite opcional para la cantidad de personajes a mostrar.
3. El sistema recupera los personajes ordenados por nivel (descendente) y, en caso de empate, por experiencia (descendente).
4. El sistema devuelve la lista ordenada de personajes con la información relevante: ID, nombre, nivel y misiones completadas.

**Flujos Alternativos**:
- **Sin personajes**: Si no hay personajes registrados, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra el ranking de personajes.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Media - Los usuarios suelen consultar regularmente el ranking para comparar su progreso.

## 2. Gestión de Misiones

### CU-M01: Crear Misión

**Actores**: Administrador

**Descripción**: Permite crear una nueva misión con sus atributos, tipo, categoría y recompensas.

**Precondiciones**: 
- El administrador debe estar autenticado en el sistema.

**Flujo Principal**:
1. El administrador solicita crear una nueva misión.
2. El sistema muestra un formulario para ingresar los datos de la misión.
3. El administrador introduce los datos de la misión:
   - Nombre (3-100 caracteres)
   - Descripción (mínimo 10 caracteres)
   - Tipo (sigilo, combate, rescate, escolta, exploración, recolección)
   - Categoría (principal o secundaria)
   - Dificultad (1-10)
   - Experiencia base
   - Recompensa en oro base
   - Fecha límite (opcional)
4. El sistema valida los datos introducidos.
5. El sistema crea la misión con estado "pendiente" y la fecha de creación actual.
6. El sistema almacena la misión en la base de datos.
7. El sistema devuelve los datos de la misión creada, incluyendo su ID único.

**Flujos Alternativos**:
- **Datos inválidos**: El sistema muestra mensajes de error específicos para cada campo que no cumpla con las validaciones.

**Postcondiciones**:
- Se crea una nueva misión en el sistema, disponible para ser asignada a personajes.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Media - Los administradores añaden misiones regularmente para mantener el contenido actualizado.

### CU-M02: Obtener Misión

**Actores**: Usuario, Administrador

**Descripción**: Permite consultar la información detallada de una misión específica.

**Precondiciones**: 
- La misión debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver los detalles de una misión específica proporcionando su ID.
2. El sistema busca la misión en la base de datos.
3. El sistema recopila toda la información de la misión: nombre, descripción, tipo, categoría, dificultad, recompensas, etc.
4. El sistema muestra todos los detalles de la misión.

**Flujos Alternativos**:
- **Misión no encontrada**: Si no existe una misión con el ID proporcionado, el sistema devuelve un mensaje de error 404.

**Postcondiciones**:
- Se muestran los datos de la misión.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Alta - Los usuarios consultan frecuentemente los detalles de las misiones.

### CU-M03: Listar Misiones

**Actores**: Usuario, Administrador

**Descripción**: Permite obtener una lista paginada de todas las misiones disponibles.

**Precondiciones**: 
- Ninguna específica.

**Flujo Principal**:
1. El usuario solicita ver la lista de misiones.
2. El usuario puede especificar parámetros de paginación opcionales (skip y limit).
3. El sistema recupera las misiones de la base de datos según los parámetros de paginación.
4. El sistema devuelve la lista de misiones con sus datos.

**Flujos Alternativos**:
- **Sin misiones**: Si no hay misiones registradas, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de misiones.

**Excepciones**:
- Parámetros de paginación inválidos: El sistema utiliza valores predeterminados (skip=0, limit=100).

**Frecuencia de uso**: Alta - Los usuarios buscan misiones disponibles constantemente.

### CU-M04: Filtrar Misiones por Tipo

**Actores**: Usuario, Administrador

**Descripción**: Permite listar misiones filtradas por su tipo (combate, sigilo, etc.).

**Precondiciones**: 
- Deben existir misiones en el sistema.

**Flujo Principal**:
1. El usuario solicita ver misiones de un tipo específico.
2. El usuario especifica el tipo de misión (combate, sigilo, rescate, escolta, exploración o recolección).
3. El usuario puede especificar parámetros de paginación opcionales (skip y limit).
4. El sistema recupera las misiones del tipo especificado según los parámetros de paginación.
5. El sistema devuelve la lista de misiones filtradas.

**Flujos Alternativos**:
- **Tipo no válido**: Si el tipo proporcionado no es válido, el sistema puede devolver un error o una lista vacía.
- **Sin misiones del tipo**: Si no hay misiones del tipo especificado, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de misiones filtrada por tipo.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Alta - Los usuarios suelen filtrar misiones por tipo para encontrar las que prefieren.

### CU-M05: Filtrar Misiones por Categoría

**Actores**: Usuario, Administrador

**Descripción**: Permite listar misiones filtradas por su categoría (principal o secundaria).

**Precondiciones**: 
- Deben existir misiones en el sistema.

**Flujo Principal**:
1. El usuario solicita ver misiones de una categoría específica.
2. El usuario especifica la categoría (principal o secundaria).
3. El usuario puede especificar parámetros de paginación opcionales (skip y limit).
4. El sistema recupera las misiones de la categoría especificada según los parámetros de paginación.
5. El sistema devuelve la lista de misiones filtradas.

**Flujos Alternativos**:
- **Categoría no válida**: Si la categoría proporcionada no es 'principal' o 'secundaria', el sistema puede devolver un error o una lista vacía.
- **Sin misiones de la categoría**: Si no hay misiones de la categoría especificada, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de misiones filtrada por categoría.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Alta - La distinción entre misiones principales y secundarias es fundamental para la progresión del juego.

### CU-M06: Filtrar Misiones por Dificultad

**Actores**: Usuario, Administrador

**Descripción**: Permite listar misiones dentro de un rango de dificultad especificado.

**Precondiciones**: 
- Deben existir misiones en el sistema.

**Flujo Principal**:
1. El usuario solicita ver misiones dentro de un rango de dificultad.
2. El usuario especifica el rango de dificultad (valores mínimo y máximo entre 1-10).
3. El usuario puede especificar parámetros de paginación opcionales (skip y limit).
4. El sistema recupera las misiones cuya dificultad se encuentra dentro del rango especificado.
5. El sistema devuelve la lista de misiones filtradas.

**Flujos Alternativos**:
- **Rango inválido**: Si el rango proporcionado no es válido, el sistema puede devolver un error o usar valores predeterminados.
- **Sin misiones en el rango**: Si no hay misiones dentro del rango especificado, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de misiones filtrada por dificultad.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Media - Los usuarios filtran por dificultad para encontrar misiones adecuadas a su nivel.

### CU-M07: Actualizar Misión

**Actores**: Administrador

**Descripción**: Permite modificar los atributos de una misión existente.

**Precondiciones**: 
- La misión debe existir en el sistema.
- El administrador debe estar autenticado.

**Flujo Principal**:
1. El administrador solicita actualizar una misión específica por su ID.
2. El sistema verifica que la misión existe.
3. El administrador proporciona los datos que desea actualizar (cualquiera de los atributos de la misión).
4. El sistema valida los datos proporcionados.
5. El sistema actualiza la información de la misión en la base de datos.
6. El sistema devuelve los datos actualizados de la misión.

**Flujos Alternativos**:
- **Misión no encontrada**: El sistema muestra un error 404.
- **Datos inválidos**: El sistema muestra mensajes de error de validación específicos para cada campo inválido.

**Postcondiciones**:
- La información de la misión se actualiza en el sistema.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Baja - Las actualizaciones de misiones son operaciones administrativas ocasionales.

### CU-M08: Eliminar Misión

**Actores**: Administrador

**Descripción**: Permite eliminar permanentemente una misión del sistema.

**Precondiciones**: 
- La misión debe existir en el sistema.
- El administrador debe estar autenticado.

**Flujo Principal**:
1. El administrador solicita eliminar una misión específica por su ID.
2. El sistema verifica que la misión existe.
3. El sistema elimina la misión de la base de datos, incluyendo todas sus relaciones (asignaciones a personajes).
4. El sistema confirma la eliminación de la misión.

**Flujos Alternativos**:
- **Misión no encontrada**: El sistema muestra un error 404.

**Postcondiciones**:
- La misión y todos sus datos relacionados se eliminan permanentemente del sistema.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.
- **Misión en uso**: Si la misión está actualmente en progreso por algún personaje, el sistema podría mostrar una advertencia o impedir su eliminación.

**Frecuencia de uso**: Muy baja - La eliminación de misiones es una operación administrativa poco común.

## 3. Gestión de Asignación y Progreso

### CU-A01: Asignar Misión a Personaje

**Actores**: Usuario

**Descripción**: Permite asignar una misión a un personaje específico y encolarla según su categoría.

**Precondiciones**: 
- El personaje debe existir en el sistema.
- La misión debe existir en el sistema.
- La misión no debe estar ya asignada al personaje.

**Flujo Principal**:
1. El usuario solicita asignar una misión específica a un personaje específico.
2. El sistema verifica que tanto el personaje como la misión existen.
3. El sistema crea una relación entre el personaje y la misión con estado "pendiente" y la fecha actual.
4. El sistema determina la categoría de la misión (principal o secundaria).
5. El sistema encola la misión en la cola correspondiente del personaje según su categoría.
6. El sistema confirma la asignación exitosa de la misión.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Misión no encontrada**: El sistema muestra un error 404.
- **Misión ya asignada**: Si la misión ya está asignada al personaje, el sistema devuelve la relación existente.

**Postcondiciones**:
- Se crea una relación personaje-misión.
- La misión se encola en la cola correspondiente del personaje.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Alta - Es una operación fundamental en el juego.

### CU-A02: Completar Misión

**Actores**: Usuario

**Descripción**: Marca una misión como completada, otorgando recompensas ajustadas por tipo y dificultad.

**Precondiciones**: 
- El personaje debe existir en el sistema.
- La misión debe existir en el sistema.
- La misión debe estar asignada al personaje con estado "pendiente".

**Flujo Principal**:
1. El usuario solicita completar una misión específica con un personaje específico.
2. El sistema verifica que la misión está asignada al personaje y está pendiente.
3. El sistema intenta desencolar la misión de la cola correspondiente del personaje.
4. El sistema actualiza el estado de la relación personaje-misión a "completada" y registra la fecha de finalización.
5. El sistema calcula las recompensas considerando:
   - Experiencia base de la misión
   - Oro base de la misión
   - Multiplicador por dificultad (1 + dificultad * 0.1)
   - Multiplicador por tipo de misión (según la tabla de multiplicadores)
6. El sistema otorga la experiencia y oro calculados al personaje.
7. El sistema incrementa el contador de misiones completadas del personaje.
8. El sistema actualiza el nivel del personaje si corresponde (según la experiencia acumulada).
9. El sistema devuelve un resumen con la información del personaje actualizado, la misión, las recompensas y los multiplicadores aplicados.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Misión no encontrada**: El sistema muestra un error 404.
- **Misión no asignada**: El sistema muestra un error indicando que la misión no está asignada al personaje.
- **Misión ya completada o cancelada**: El sistema muestra un error indicando que la misión ya no está pendiente.
- **La misión no está en la cola**: El sistema continúa con la actualización de estado y recompensas.

**Postcondiciones**:
- El estado de la misión cambia a "completada".
- El personaje recibe las recompensas correspondientes.
- La misión se desencolada de la cola correspondiente.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Muy alta - Es la principal forma de progresión en el juego.

### CU-A03: Completar Primera Misión en Cola

**Actores**: Usuario

**Descripción**: Completa la primera misión disponible en la cola (principal o secundaria).

**Precondiciones**: 
- El personaje debe existir en el sistema.
- El personaje debe tener al menos una misión en alguna de sus colas.

**Flujo Principal**:
1. El usuario solicita completar la primera misión disponible para un personaje específico.
2. El sistema verifica que el personaje existe.
3. El sistema intenta obtener la primera misión de la cola principal.
4. Si la cola principal está vacía, el sistema intenta obtener la primera misión de la cola secundaria.
5. Si ambas colas están vacías, el sistema muestra un mensaje indicando que no hay misiones pendientes.
6. Si encuentra una misión, el sistema la desencola de la cola correspondiente.
7. El sistema actualiza el estado de la relación personaje-misión a "completada" y registra la fecha de finalización.
8. El sistema calcula y otorga las recompensas considerando los multiplicadores por tipo y dificultad.
9. El sistema incrementa el contador de misiones completadas del personaje.
10. El sistema actualiza el nivel del personaje si corresponde.
11. El sistema devuelve un resumen con la información del personaje actualizado, la misión y las recompensas.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Ambas colas vacías**: El sistema muestra un mensaje indicando que el personaje no tiene misiones pendientes.

**Postcondiciones**:
- El estado de la primera misión cambia a "completada".
- El personaje recibe las recompensas correspondientes.
- La misión se desencolada de la cola correspondiente.

**Excepciones**:
- Error al desencolar: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Muy alta - Es una forma conveniente de completar misiones en orden.

### CU-A04: Cancelar Misión

**Actores**: Usuario

**Descripción**: Marca una misión como cancelada para un personaje, desacolándola si está en la cola.

**Precondiciones**: 
- El personaje debe existir en el sistema.
- La misión debe existir en el sistema.
- La misión debe estar asignada al personaje con estado "pendiente".

**Flujo Principal**:
1. El usuario solicita cancelar una misión específica con un personaje específico.
2. El sistema verifica que la misión está asignada al personaje y está pendiente.
3. El sistema intenta desencolar la misión de la cola correspondiente del personaje.
4. El sistema actualiza el estado de la relación personaje-misión a "cancelada" y registra la fecha de finalización.
5. El sistema incrementa el contador de misiones canceladas del personaje.
6. El sistema confirma la cancelación exitosa de la misión.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Misión no encontrada**: El sistema muestra un error 404.
- **Misión no asignada**: El sistema muestra un error indicando que la misión no está asignada al personaje.
- **Misión ya completada o cancelada**: El sistema muestra un error indicando que la misión ya no está pendiente.
- **La misión no está en la cola**: El sistema continúa con la actualización de estado.

**Postcondiciones**:
- El estado de la misión cambia a "cancelada".
- Se incrementa el contador de misiones canceladas del personaje.
- La misión se desencolada de la cola correspondiente si estaba en ella.

**Excepciones**:
- Error en la base de datos: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Baja a media - Los jugadores suelen preferir completar misiones que cancelarlas.

### CU-A05: Listar Misiones de Personaje

**Actores**: Usuario

**Descripción**: Obtiene todas las misiones asignadas a un personaje con filtro opcional por estado.

**Precondiciones**: 
- El personaje debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver las misiones asignadas a un personaje específico.
2. El usuario puede especificar un filtro opcional por estado (pendiente, completada o cancelada).
3. El sistema verifica que el personaje existe.
4. El sistema recupera todas las relaciones personaje-misión para el personaje especificado, aplicando el filtro si se proporcionó.
5. El sistema extrae la información de las misiones asociadas.
6. El sistema devuelve la lista de misiones del personaje.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Sin misiones**: Si el personaje no tiene misiones asignadas que cumplan con el filtro, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de misiones del personaje, opcionalmente filtrada por estado.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Alta - Los usuarios consultan frecuentemente sus misiones asignadas.

### CU-A06: Listar Personajes por Misión

**Actores**: Usuario, Administrador

**Descripción**: Obtiene todos los personajes que tienen asignada una misión específica.

**Precondiciones**: 
- La misión debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver los personajes asignados a una misión específica.
2. El usuario puede especificar un filtro opcional por estado (pendiente, completada o cancelada).
3. El sistema verifica que la misión existe.
4. El sistema recupera todas las relaciones personaje-misión para la misión especificada, aplicando el filtro si se proporcionó.
5. El sistema extrae la información de los personajes asociados.
6. El sistema devuelve la lista de personajes con la misión asignada.

**Flujos Alternativos**:
- **Misión no encontrada**: El sistema muestra un error 404.
- **Sin personajes**: Si la misión no está asignada a ningún personaje que cumpla con el filtro, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista de personajes con la misión asignada, opcionalmente filtrada por estado.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Baja - Principalmente útil para administradores o para estadísticas del juego.

## 4. Gestión de Colas de Misiones

### CU-C01: Consultar Cola de Misiones

**Actores**: Usuario

**Descripción**: Obtiene información sobre el estado de una cola de misiones (principal o secundaria).

**Precondiciones**: 
- El personaje debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver el estado de una cola específica (principal o secundaria) para un personaje específico.
2. El sistema verifica que el personaje existe.
3. El sistema verifica que el tipo de cola sea válido ('principal' o 'secundaria').
4. El sistema recupera la información de la cola:
   - Si está vacía
   - Tamaño (número de misiones)
   - Próxima misión (la primera en la cola)
5. El sistema devuelve la información de la cola.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Tipo de cola inválido**: El sistema muestra un error 400.
- **Cola vacía**: El sistema indica que la cola está vacía y que no hay próxima misión.

**Postcondiciones**:
- Se muestra la información de la cola de misiones.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Media - Los usuarios consultan sus colas para planificar su progresión.

### CU-C02: Obtener Misiones en Orden FIFO

**Actores**: Usuario

**Descripción**: Lista todas las misiones de un personaje ordenadas según su posición en las colas.

**Precondiciones**: 
- El personaje debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver las misiones de un personaje específico en orden FIFO.
2. El sistema verifica que el personaje existe.
3. El sistema obtiene la cola principal del personaje.
4. El sistema obtiene la cola secundaria del personaje.
5. El sistema extrae las misiones de ambas colas, manteniendo el orden FIFO dentro de cada cola.
6. El sistema devuelve primero las misiones de la cola principal, seguidas de las misiones de la cola secundaria.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Ambas colas vacías**: El sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra la lista ordenada de misiones según el principio FIFO, primero las misiones principales y luego las secundarias.

**Excepciones**:
- Error al acceder a las colas: El sistema muestra un mensaje de error adecuado.

**Frecuencia de uso**: Media - Los usuarios consultan sus misiones en orden para planificar su progresión.

## 5. Consultas y Reportes

### CU-R01: Obtener Estadísticas de Personaje

**Actores**: Usuario

**Descripción**: Consulta estadísticas detalladas de un personaje: nivel, experiencia, oro, misiones completadas.

**Precondiciones**: 
- El personaje debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver las estadísticas detalladas de un personaje específico.
2. El sistema verifica que el personaje existe.
3. El sistema recopila todas las estadísticas del personaje:
   - Información básica (nombre, ID)
   - Nivel y experiencia
   - Salud y maná
   - Oro acumulado
   - Contador de misiones completadas y canceladas
4. El sistema devuelve las estadísticas completas del personaje.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.

**Postcondiciones**:
- Se muestran las estadísticas detalladas del personaje.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Alta - Los usuarios consultan frecuentemente sus estadísticas.

### CU-R02: Obtener Historial de Misiones

**Actores**: Usuario

**Descripción**: Obtiene un historial de todas las misiones realizadas por un personaje.

**Precondiciones**: 
- El personaje debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver el historial de misiones de un personaje específico.
2. El sistema verifica que el personaje existe.
3. El sistema recupera todas las relaciones personaje-misión para el personaje especificado.
4. El sistema extrae la información completa de cada misión, incluyendo:
   - Datos básicos de la misión (nombre, descripción, tipo)
   - Estado (pendiente, completada, cancelada)
   - Fechas de asignación y finalización (si aplica)
5. El sistema devuelve la lista completa de misiones.

**Flujos Alternativos**:
- **Personaje no encontrado**: El sistema muestra un error 404.
- **Sin misiones**: Si el personaje no tiene misiones asignadas, el sistema devuelve una lista vacía.

**Postcondiciones**:
- Se muestra el historial completo de misiones del personaje.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Media - Los usuarios consultan ocasionalmente su historial de misiones.

### CU-R03: Consultar Recompensas Potenciales

**Actores**: Usuario

**Descripción**: Permite ver las recompensas disponibles por completar una misión específica.

**Precondiciones**: 
- La misión debe existir en el sistema.

**Flujo Principal**:
1. El usuario solicita ver los detalles de una misión específica.
2. El sistema muestra los detalles completos de la misión, incluyendo:
   - Experiencia base
   - Oro base
   - Dificultad (que afecta al multiplicador)
   - Tipo de misión (que determina el multiplicador específico)
3. El usuario puede calcular mentalmente o el sistema puede mostrar las recompensas finales considerando los multiplicadores.

**Flujos Alternativos**:
- **Misión no encontrada**: El sistema muestra un error 404.

**Postcondiciones**:
- Se muestran las recompensas potenciales de la misión.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Alta - Los usuarios evalúan las recompensas antes de aceptar misiones.

## 6. Administración del Sistema

### CU-S01: Inicialización del Sistema

**Actores**: Sistema

**Descripción**: Inicializa el sistema y crea las tablas de base de datos si no existen.

**Precondiciones**: 
- La base de datos debe estar configurada correctamente.
- Las credenciales de acceso deben ser válidas.

**Flujo Principal**:
1. El sistema inicia la aplicación.
2. El sistema establece una conexión con la base de datos.
3. El sistema verifica si las tablas necesarias existen.
4. Si las tablas no existen, el sistema las crea según los modelos definidos.
5. El sistema confirma la inicialización correcta.

**Flujos Alternativos**:
- **Error de conexión**: El sistema muestra un mensaje de error y termina la ejecución.
- **Error al crear tablas**: El sistema muestra un mensaje de error detallado.

**Postcondiciones**:
- Las tablas necesarias existen en la base de datos.
- El sistema está listo para funcionar.

**Excepciones**:
- Errores de base de datos: El sistema muestra mensajes de error adecuados.

**Frecuencia de uso**: Muy baja - Solo ocurre al iniciar la aplicación por primera vez o después de cambios en los modelos.

### CU-S02: Consultar Documentación API

**Actores**: Desarrollador

**Descripción**: Accede a la documentación interactiva de la API (Swagger).

**Precondiciones**: 
- La aplicación debe estar en ejecución.

**Flujo Principal**:
1. El desarrollador accede a la ruta `/docs`.
2. El sistema genera y muestra la interfaz Swagger UI.
3. La interfaz muestra todos los endpoints disponibles, agrupados por tags.
4. Cada endpoint muestra:
   - Método HTTP
   - Ruta
   - Descripción
   - Parámetros requeridos y opcionales
   - Esquema de respuesta
   - Códigos de estado posibles
5. El desarrollador puede probar los endpoints directamente desde la interfaz.

**Flujos Alternativos**:
- **Error al cargar Swagger**: El sistema muestra un mensaje de error.

**Postcondiciones**:
- Se muestra la documentación interactiva de la API.

**Excepciones**:
- Ninguna específica.

**Frecuencia de uso**: Baja - Principalmente utilizada durante el desarrollo y pruebas.
