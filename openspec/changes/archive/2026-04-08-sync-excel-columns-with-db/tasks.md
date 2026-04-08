## 1. Agregar columnas al Excel de detecciones

- [x] 1.1 En `anonymizer/mapping.py`, función `save_extended_excel` (L122): agregar "Aliases" y "Modo" a la lista `headers`.
- [x] 1.2 En el loop de escritura de filas (L130-143): escribir `row_dict.get("aliases", "")` en col 7 y `row_dict.get("modo", "palabra")` en col 8.
- [x] 1.3 Agregar anchos de columna: `ws.column_dimensions["G"].width = 40` y `ws.column_dimensions["H"].width = 14`.
- [x] 1.4 Extender el rango de coloreo verde para filas DB (L142): `range(1, 9)` en lugar de `range(1, 7)`.

## 2. Actualizar lectura del Excel

- [x] 2.1 En `anonymizer/mapping.py`, función `load_extended_data` (L157-187): leer columnas 7 y 8 de forma opcional.
- [x] 2.2 Si `len(row) >= 7`: extraer `aliases_raw = str(row[6])`, parsear con `split(",")` en lista. Si no existe, default `[]`.
- [x] 2.3 Si `len(row) >= 8`: extraer `modo = str(row[7]).strip().lower()`. Si no existe o inválido, default `"palabra"`.
- [x] 2.4 Incluir `"aliases"` (list[str]) y `"modo"` (str) en cada dict de resultado.

## 3. Actualizar guardado a DB desde GUI

- [x] 3.1 En `anonymizer/gui.py`, método `_apply_thread` (L223-233): al crear `KnownEntity`, pasar `aliases=d.get("aliases", [])` y `match_mode=d.get("modo", "palabra")`.

## 4. Actualizar guardado a DB desde CLI

- [x] 4.1 En `anonymizer/cli.py`, en el flujo de aplicación: al crear `KnownEntity` desde datos del Excel, pasar aliases y match_mode del row.

## 5. Actualizar hoja de instrucciones

- [x] 5.1 En `_create_instruction_sheet` (L70-110): la documentación de Aliases y Modo ya existe en las líneas 95-99. Verificar que sigue siendo correcta y coherente con el nuevo esquema unificado.

## 6. Validación

- [x] 6.1 Generar un Excel de detecciones y verificar que contiene 8 columnas con headers correctos.
- [x] 6.2 Abrir un Excel antiguo (6 columnas) y verificar que se lee sin error, con defaults para aliases y modo.
- [x] 6.3 Llenar aliases y modo en el Excel, marcar "Guardar DB = s", aplicar, y verificar que la entidad se guarda completa en la DB maestra con los aliases y modo especificados.
- [x] 6.4 Exportar la DB maestra a Excel y confirmar que la entidad guardada tiene aliases y modo correctos.
