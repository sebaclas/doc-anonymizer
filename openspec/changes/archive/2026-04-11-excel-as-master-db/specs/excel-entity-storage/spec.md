## ADDED Requirements

### Requirement: Persistencia en Formato Excel (.xlsx)
El sistema SHALL utilizar un archivo Excel (.xlsx) como repositorio primario y único de entidades conocidas en el directorio del usuario.

#### Scenario: Creación de archivo inicial
- **WHEN** el sistema se inicia y no encuentra el archivo de base de datos maestra en formato Excel
- **THEN** el sistema SHALL crear un nuevo archivo Excel con las cabeceras estándar (Original, Pseudonimo, Tipo, Aliases, Modo).

### Requirement: Sincronización Automática al Detectar
El sistema SHALL cargar los datos del archivo Excel en memoria antes de cada proceso de detección de entidades.

#### Scenario: Detección con cambios manuales en Excel
- **WHEN** el usuario modifica o guarda el archivo Excel y luego inicia una detección
- **THEN** el sistema SHALL aplicar exactamente las entradas presentes en el Excel en ese momento.

### Requirement: Eliminación de Entidades vía Excel
Al ser el Excel la única fuente de verdad, cualquier fila eliminada del archivo SHALL considerarse eliminada del sistema.

#### Scenario: Borrado de una entidad conocida
- **WHEN** un usuario elimina una fila del archivo Excel y guarda los cambios
- **THEN** esa entidad SHALL dejar de ser detectada proactivamente en los siguientes procesamientos.
