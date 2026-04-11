# Tasks: GUI Regex Editor (Single List Model)

## 1. Migración y Persistencia de Patrones
- [x] 1.1 Definir lista `DEFAULT_PATTERNS` en `anonymizer/detectors/patterns.py` (incluyendo DNI, Email, CUIT y templates como Expediente).
- [x] 1.2 En `anonymizer/config.py`, implementar lógica para inicializar `custom_patterns.json` con la lista de fábrica en la primera ejecución.
- [x] 1.3 Refactorizar `patterns.detect()` para que use exclusivamente la lista cargada desde el JSON.

## 2. Ventana del Editor de Regex (Unificada)
- [x] 2.1 Crear `anonymizer/regex_editor.py` con una lista principal (usando `CTkScrollableFrame`) que muestre todos los patrones.
- [x] 2.2 Cada fila de la lista permite: Activar/Desactivar (switch), Ver detalles, Eliminar.
- [x] 2.3 Botón "Nuevo Patrón" para limpiar el panel de edición y crear uno desde cero.

## 3. Panel de Edición y Prueba en Vivo
- [x] 3.1 Al seleccionar un patrón de la lista, se carga en el panel de edición.
- [x] 3.2 Campos: Nombre, Tipo (EntityType), Regex.
- [x] 3.3 TextArea de "Texto de ejemplo" para prueba en vivo.
- [x] 3.4 Resaltado de matches y validación de sintaxis regex.

## 4. Integración y Validación
- [x] 4.1 Agregar botón de acceso en la GUI principal.
- [x] 4.2 Botón de "Restaurar por defecto" en el editor para recuperar patrones eliminados de fábrica.
- [x] 4.3 Validar que los cambios se persisten correctamente y se aplican en la siguiente detección.
- [x] 4.4 Verificar que desactivar un patrón funciona (deja de detectarse sin borrarlo).
- [x] 4.5 Asegurar que los patrones built-in tienen un `id` fijo para facilitar futuras actualizaciones de la app.
