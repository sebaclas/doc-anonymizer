## Context

El sistema actual utiliza un modelo de sincronización bidireccional entre un JSON local (`known_entities.json`) y un Excel editable. El JSON permite una carga rápida para el motor de detección, mientras que el Excel ofrece una interfaz amigable para el usuario. Sin embargo, el proceso de "importación" actual es acumulativo (upsert), lo que impide borrar registros desde el Excel. Además, el uso de archivos temporales complica la persistencia de cambios directos.

## Goals / Non-Goals

**Goals:**
- Establecer el archivo Excel como la única fuente de verdad para entidades conocidas.
- Permitir la eliminación de registros directamente desde el Excel.
- Eliminar la necesidad de procesos de importación manuales en la GUI.
- Mantener el rendimiento de la detección mediante una caché en memoria cargada al inicio.

**Non-Goals:**
- Implementar un editor de celdas integrado en la GUI (se seguirá usando Microsoft Excel).
- Soporte para bases de datos SQL en esta etapa.

## Decisions

### 1. Cambio de almacenamiento primario a .xlsx
- **Decisión**: Reemplazar `known_entities.json` por `known_entities.xlsx` como el archivo de persistencia en `~/.doc-anonymizer/`.
- **Razón**: Los usuarios prefieren y entienden el manejo de hojas de cálculo para datos masivos.
- **Alternativa considerada**: Cambiar la lógica del importador JSON para detectar borrados (diffing). **Rechazado** por ser más complejo de mantener y propenso a errores de estado.

### 2. Carga en Memoria (Startup / Cache)
- **Decisión**: El motor de detección cargará todas las filas del Excel en una lista de objetos `KnownEntity` al inicio de cada proceso de anonimización.
- **Razón**: `openpyxl` es lento para consultas frecuentes. Cargar en memoria asegura que la detección sea instantánea una vez iniciada la carga inicial.

### 3. Manejo de Bloqueos de Archivo (File Locks)
- **Decisión**: Implementar un bloque `try-except PermissionError` al intentar guardar nuevas entidades desde la App. Si el Excel está abierto por el usuario, se mostrará un aviso pidiéndole que lo cierre y guarde sus cambios antes de que la App pueda escribir.
- **Razón**: Excel bloquea el archivo para escritura cuando está abierto. Es una restricción del SO que debemos manejar con UX.

## Risks / Trade-offs

- **[Riesgo] Corrupción de archivo binario** → **Mitigación**: Realizar un backup automático (`.bak`) cada vez que la App realice una escritura exitosa en el Excel.
- **[Riesgo] Dependencia de `openpyxl`** → **Mitigación**: Asegurar que las dependencias estén bien gestionadas y que el formato del Excel sea simple (sin macros ni formatos complejos que rompan el parser).
- **[Trade-off] Velocidad de arranque** → El inicio de la detección podría tardar unos milisegundos más mientras se parsea el Excel, pero la experiencia global de edición es superior.
