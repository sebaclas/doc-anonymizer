## Why

El Excel de detecciones (generado al analizar un documento) y el Excel de la Base de Datos Maestra tienen esquemas de columnas diferentes. Cuando el usuario marca "Guardar DB = s" en el Excel de detecciones, la entidad se inserta en la DB sin aliases ni modo de coincidencia, porque esas columnas no existen en el Excel de detecciones. Esto obliga al usuario a abrir la DB Maestra por separado para completar esos campos.

Diferencia actual de esquemas:

| Columna | Excel Detecciones | Excel DB Maestra |
|---------|-------------------|------------------|
| Original | ✅ col 1 | ✅ col 1 |
| Tipo | ✅ col 2 | ✅ col 3 |
| Pseudónimo | ✅ col 3 | ✅ col 2 |
| Acción | ✅ col 4 | ❌ no existe |
| Guardar DB | ✅ col 5 | ❌ no existe |
| Origen | ✅ col 6 | ❌ no existe |
| Aliases | ❌ no existe | ✅ col 4 |
| Modo | ❌ no existe | ✅ col 5 |

Unificar las columnas permite un flujo de un solo paso: detectar, revisar, completar *todos* los atributos (incluyendo aliases y modo), y al marcar "Guardar DB" la entidad se inserta completa en la base de datos maestra.

## What Changes

- Agregar columnas "Aliases" y "Modo" al Excel de detecciones (`save_extended_excel` en `mapping.py`).
- Actualizar `load_extended_data` para leer las nuevas columnas de forma retrocompatible.
- Modificar el flujo de guardado a DB (en `gui.py` y `cli.py`) para pasar aliases y modo al crear `KnownEntity`.
- Esquema final del Excel de detecciones: `Original | Tipo | Pseudónimo | Acción | Guardar DB | Origen | Aliases | Modo`.
- Actualizar la hoja de instrucciones del Excel para documentar las nuevas columnas.

## Capabilities

### New Capabilities

- Ninguna (extensión de capacidades existentes).

### Modified Capabilities

- `excel-workflow`: El Excel de detecciones incluye ahora columnas "Aliases" y "Modo", alineadas con el esquema de la DB Maestra.
- `gui-workflow`: Al marcar "Guardar DB = s", se pasan aliases y modo desde el Excel al crear `KnownEntity`.
- `cli-workflow`: Ídem para el flujo CLI.

## Impact

- `anonymizer/mapping.py`: Funciones `save_extended_excel`, `load_extended_data`, `_create_instruction_sheet`.
- `anonymizer/gui.py`: Método `_apply_thread` — pasar aliases y modo al crear `KnownEntity`.
- `anonymizer/cli.py`: Comando de aplicación — pasar aliases y modo.
- Retrocompatible: Excels existentes sin las nuevas columnas seguirán funcionando (columnas opcionales al leer).
