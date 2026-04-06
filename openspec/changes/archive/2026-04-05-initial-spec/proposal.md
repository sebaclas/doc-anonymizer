## Why

Formalizar la especificación y diseño del proyecto `doc-anonymizer` en el marco de OpenSpec. Esto permitirá tener un registro claro de las capacidades, decisiones arquitectónicas y dependencias, facilitando el desarrollo y mantenimiento futuro basándose en la funcionalidad actual.

## What Changes

- Creación de documentación de especificaciones (specs) basadas en las funcionalidades actuales descritas en `MANUAL.md` (CLI, Extracción, NER, Regex, Matching contra DB de entidades conocidas, y Reemplazo).
- Creación de documento de diseño arquitectónico (design) basado en `STACK.md` y estructura de módulos subyacente.

## Capabilities

### New Capabilities
- `cli-workflow`: Flujos del CLI (`run`, `detect`, `apply`, `db`) y sus opciones.
- `document-processing`: Procesamiento de documentos (lectura de Word/PDF, extracción, y regeneración de salida).
- `entity-detection`: Detección de entidades usando Inteligencia Artificial (NER vía spaCy) y expresiones regulares (patrones).
- `entity-matching`: Matching contra base de datos (búsqueda exacta y aproximada con rapidfuzz) y revisión interactiva tipo prompt-based.

### Modified Capabilities

## Impact

- Establece la línea base de especificaciones (`specs`) y arquitectura (`design`), lo que servirá para guiar el agregado de futuras funcionalidades bajo un proceso de ingeniería de software sólido. No altera el código implementado, solo se documenta su estructura actual de manera estandarizada y se integra en el flujo OpenSpec.
