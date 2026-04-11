## Why

Actualmente, el sistema mantiene una sincronización parcial entre el archivo JSON (`known_entities.json`) y el archivo Excel Maestro. Esto causa confusión cuando el usuario borra registros en Excel pero estos persisten en el JSON. Al convertir el Excel en la única fuente de verdad (Single Source of Truth), eliminamos la ambigüedad y aseguramos que lo que el usuario ve en el Excel es exactamente lo que el motor de detección utiliza.

## What Changes

- **Transición de Fuente de Verdad**: El archivo `known_entities.json` será deprecado como base de datos primaria. El motor de detección cargará las entidades directamente desde un archivo Excel persistente.
- **Persistencia Directa**: La gestión de la base de datos desde la GUI abrirá el archivo real ubicado en el directorio de la aplicación, eliminando el uso de archivos temporales.
- **Sincronización Automática**: El motor de detección detectará si el archivo Excel ha sido modificado y recargará los datos antes de cada proceso de anonimización.
- **Mapeo Unificado**: Se simplificará el flujo de importación/exportación al no existir un paso intermedio de JSON.

## Capabilities

### New Capabilities
- `excel-entity-storage`: Gestión persistente de entidades conocidas directamente en formato Excel corporativo.

### Modified Capabilities
- `entity-detection`: El proceso de detección ahora consultará la fuente de verdad en Excel en lugar del JSON local.

## Impact

- `anonymizer/known_entities.py`: Refactorización completa de los métodos de carga, guardado e importación.
- `anonymizer/detectors/detector.py`: Cambio en la fuente de carga inicial de patrones conocidos.
- `anonymizer/gui.py`: Actualización del botón de gestión para abrir el archivo persistente y manejar posibles bloqueos de archivo (file locks).
- `anonymizer/config.py`: Cambio en las rutas de configuración para apuntar al archivo `.xlsx` por defecto.
