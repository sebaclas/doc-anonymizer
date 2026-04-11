## 1. Migración de Rutas y Configuración

- [x] 1.1 Actualizar `anonymizer/config.py` para definir `master_db.xlsx` como la ruta por defecto para la base maestra.
- [x] 1.2 Deprecar la referencia a `known_entities.json` en los ajustes por defecto.
- [x] 1.3 Implementar una migración única automática: si existe `known_entities.json`, volcar su contenido al nuevo `master_db.xlsx`.

## 2. Refactorización de `known_entities.py`

- [x] 2.1 Modificar `load()` para que lea directamente del archivo Excel usando `from_excel`.
- [x] 2.2 Reimplementar `save()` y `add()` para que escriban directamente en el Excel.
- [x] 2.3 Implementar manejo de `PermissionError` en escrituras (cuando Excel tiene el archivo abierto).
- [x] 2.4 Eliminar funciones obsoletas de manejo de archivos temporales.

## 3. Integración en el Motor de Detección y GUI

- [x] 3.1 Actualizar `anonymizer/detectors/detector.py` para que cargue la "Database" desde el Excel al inicio de `detect_all`.
- [x] 3.2 Modificar `anonymizer/gui.py` para que el botón de gestión abra directamente el archivo `.xlsx` persistente.
- [x] 3.3 El botón ahora dirá "Abrir Base de Datos Maestra" (sin mencionar archivos temporales).

## 4. Validación y Pruebas

- [x] 4.1 Verificar que las eliminaciones en Excel se reflejen en la detección (Target principal del cambio).
- [x] 4.2 Validar que el guardado automático desde la detección a la DB maestra funciona (siempre que el Excel esté cerrado).
- [x] 4.3 Comprobar integridad de datos al migrar del sistema viejo al nuevo.
