# Design: Master Database Improvement

## Database Location
- User local path: `~/.doc-anonymizer/known_entities.json`.
- On start, the app will verify it exists, and if not, it will create an empty JSON file (`[]`).

## Excel Workflow Changes
- The `save_extended_excel` function in `mapping.py` will add a sixth column: `Guardar en DB?`.
- During `apply`, the code will check this column. If `s`, it will call `known_entities.add(...)`.

## GUI Changes
- **New Sidebar/Tab or Button Area**: Add a "Base de Datos" section.
- **Action Buttons**:
  - `Abrir DB Maestra (Excel)`: Calls `ke_module.to_excel()` to a temp file, opens it.
  - `Sincronizar cambios`: Calls `ke_module.from_excel()`.

## Packaging
- The bundled `known_entities.json` (inside the EXE) will act as a "restore factory settings" fallback, or we can just stick to the local user file.
