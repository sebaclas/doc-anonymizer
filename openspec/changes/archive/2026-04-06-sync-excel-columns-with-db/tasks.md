## 1. Agregar columnas al Excel de detecciones

## 1. Agregar columnas al Excel de detecciones

- [x] 1.1 En `anonymizer/mapping.py`, actualizar `save_extended_excel` para agregar headers "Aliases" (col 7) y "Modo" (col 8).
- [x] 1.2 En `save_extended_excel`, escribir los valores `aliases` y `modo` de cada `row_dict` en las columnas correspondientes.
- [x] 1.3 Ajustar los anchos de columna para las nuevas columnas (Aliases=40, Modo=14).

## 2. Actualizar lectura del Excel

- [x] 2.1 En `anonymizer/mapping.py`, actualizar `load_extended_data` para leer las columnas 7 y 8 de forma opcional (si existen).
- [x] 2.2 Devolver `aliases` (list[str]) y `modo` (str) en cada dict de resultado, con defaults vacío y "palabra".

## 3. Actualizar guardado a DB

- [x] 3.1 En `anonymizer/gui.py`, método `_apply_thread`: al crear `KnownEntity` desde datos del Excel, pasar `aliases` y `match_mode` del row.
- [x] 3.2 En `anonymizer/cli.py`, comando de aplicación: ídem, pasar aliases y match_mode al crear `KnownEntity`.

## 4. Actualizar instrucciones

- [x] 4.1 En `_create_instruction_sheet`, agregar documentación para las columnas "Aliases" y "Modo" con ejemplos de uso.

## 5. Validación

- [x] 5.1 Verificar que un Excel generado contiene las 8 columnas correctas.
- [x] 5.2 Verificar que un Excel antiguo (6 columnas) se lee correctamente sin errores.
- [x] 5.3 Verificar que al marcar "Guardar DB = s" con aliases y modo definidos, la entidad se guarda completa en la DB maestra.
