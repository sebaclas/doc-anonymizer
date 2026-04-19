## Why

Actualmente el modelo NER principal (spaCy) tiene limitaciones y omisiones notables en la detección de cantidades y montos monetarios escritos enteramente en lenguaje natural. Se requiere introducir una capa de redundancia (safety net) que funcione tanto para español como para inglés, extrayendo de manera confiable números escritos (ej. "doscientos mil", "cien", "twenty-two") para no dejar escapar información sensible u observable; tolerando proactivamente falsos positivos, dado que el proceso pasa por revisión manual.

## What Changes

- Se integrará un nuevo pipeline de detección soportado en la librería `text2num` (versión 3.x) que extrae números escritos en texto.
- Se creará un nuevo módulo detector `amount.py` (o similar) que se invocará en la fase de `detect_all` en `detector.py`.
- Se modificarán las dependencias del proyecto (`pyproject.toml` o `requirements.txt`) para contemplar la librería externa pre-compilada.

## Capabilities

### New Capabilities
- `amount-detection`: Detección en frío de montos y cantidades escritas en lenguaje natural multidioma, con extracción del valor matemático crudo para contexto.

### Modified Capabilities
- (No hay cambios directos en los modulos de sustitución o sanitización profunda, solo amplía la detección de entidades).

## Impact

- Modificación de la cadena de detección global en `anonymizer/detectors/detector.py` unificando prioridades entre NER, regex y now text2num.
- Agregado de `text2num` a las dependencias.
- Es necesario validar que el ejecutable estandar de Windows (vía PyInstaller / file `AnonymizerPro.spec`) empaquete correctamente el wheel de `text2num` ya que su core usa binarios de Rust subyacentes.
