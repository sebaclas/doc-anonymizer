## Why

El Excel de detecciones (generado al analizar un documento) y el Excel de la Base de Datos Maestra tienen esquemas de columnas diferentes. Esto impide que el usuario pueda definir atributos avanzados (aliases, modo de coincidencia) directamente desde el Excel de detecciones al momento de marcar "Guardar DB = s". Actualmente, cuando se guarda una entidad en la DB desde el Excel de detecciones, se pierde la oportunidad de asignar aliases y modo de match, obligando al usuario a abrir la DB Maestra por separado para completar esos campos.

Unificar las columnas del Excel de detecciones con las de la DB permite un flujo de trabajo más eficiente: el usuario detecta, revisa, completa *todos* los atributos (incluyendo aliases y modo) en un solo paso, y al marcar "Guardar DB" la entidad se inserta completa en la base de datos maestra.

## What Changes

- Agregar columnas "Aliases" y "Modo" al Excel de detecciones (`save_extended_excel`).
- Actualizar `load_extended_data` para leer las nuevas columnas.
- Modificar el flujo de guardado a DB (en `gui.py` y `cli.py`) para pasar aliases y modo al crear `KnownEntity`.
- Unificar el orden de columnas: `Original | Tipo | Pseudónimo | Acción | Guardar DB | Origen | Aliases | Modo`.
- Actualizar la hoja de instrucciones del Excel para documentar las nuevas columnas.

## Capabilities

### New Capabilities

- Ninguna (solo extensión de capacidades existentes)

### Modified Capabilities

- `excel-workflow`: El Excel de detecciones incluye ahora columnas "Aliases" y "Modo", alineadas con el esquema de la DB Maestra.
- `gui-workflow`: Al guardar a DB, se pasan los campos de Aliases y Modo desde el Excel.
- `cli-workflow`: Ídem para el flujo CLI.

## Impact

- `anonymizer/mapping.py`: Funciones `save_extended_excel`, `load_extended_data`, `_create_instruction_sheet`.
- `anonymizer/gui.py`: Método `_apply_thread` para pasar aliases y modo al crear `KnownEntity`.
- `anonymizer/cli.py`: Comando de aplicación para pasar aliases y modo.
- Retrocompatible: Excels existentes sin las nuevas columnas seguirán funcionando (las columnas nuevas son opcionales al leer).
