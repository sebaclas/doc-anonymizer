## Why

Actualmente, los patrones regex personalizados solo pueden configurarse editando manualmente el archivo `custom_patterns.json`. Esto requiere conocimiento técnico de JSON y regex, excluyendo a usuarios no técnicos. Además, no hay forma de probar un patrón regex antes de usarlo, lo que lleva a errores silenciosos o detecciones incorrectas.

Se necesita una interfaz gráfica accesible para que cualquier usuario pueda:
1. Ver los patrones activos (built-in y custom).
2. Agregar/editar/eliminar patrones custom con validación visual.
3. Probar un patrón contra texto de ejemplo antes de guardarlo.
4. Activar/desactivar templates predefinidos comunes.
5. Externalizar patrones built-in (hardcodeados) para que sean gestionables desde la configuración.

## What Changes

- Crear una ventana secundaria `RegexEditorWindow` accesible desde la GUI principal.
- Implementar campo de prueba: el usuario escribe un patrón y un texto de ejemplo, ve los matches destacados en tiempo real.
- Agregar templates predefinidos (Nro. expediente, Nro. cuenta, Nro. contrato, etc.) que se activan con un checkbox.
- Persistir los patrones custom en `~/.doc-anonymizer/custom_patterns.json`.
- Cargar los patrones automáticamente al ejecutar la detección.

## Capabilities

### New Capabilities

- `regex-editor-gui`: Ventana secundaria para gestionar patrones regex custom con prueba en vivo.
- `regex-templates`: Catálogo de patrones predefinidos comunes que el usuario puede activar/desactivar.

### Modified Capabilities

- `gui-workflow`: Nuevo botón para acceder al editor de regex desde la pantalla principal.
- `detection-patterns`: Los patrones custom se cargan automáticamente desde JSON al correr la detección.

## Impact

- `anonymizer/gui.py`: Nuevo botón de acceso + instanciación de `RegexEditorWindow`.
- `anonymizer/regex_editor.py` (NUEVO): Ventana CustomTkinter completa.
- `anonymizer/detectors/patterns.py`: Agregar lista de templates predefinidos con flag de activación.
- `anonymizer/config.py`: Funciones para cargar/guardar `custom_patterns.json`.
- Tamaño de la app: sin cambio significativo (sin nuevas dependencias).
