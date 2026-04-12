## Why

Currently, users must manually assign pseudonyms to every new entity detected that is not already in the Known Entities Database. This is time-consuming for large documents with many unique entities. Providing automatic, pattern-based pseudonyms (e.g., Persona1, Persona2, Org1, Org2) provides a "sane default" that speeds up the workflow, especially for large documents with many unique entities, and ensures a consistent naming convention without requiring user creativity for every instance.

## What Changes

- **Sugerencias en Excel**: Al generar el Excel de mapeo, la columna `Pseudonimo` se completará automáticamente con una sugerencia (ej: Persona1). Esto ahorra tiempo de escritura, pero el usuario mantiene el control total para cambiar, borrar o ignorar estas sugerencias en el archivo Excel antes de aplicar la anonimización.
- **Sugerencias en CLI**: En el modo interactivo del CLI, el sistema sugerirá el pseudónimo automático como valor predeterminado, permitiendo al usuario aceptarlo con un Enter o ingresar uno distinto.
- **Garantía de Unicidad (Sugerencias)**: El generador asegurará que, como punto de partida, textos idénticos reciban la misma sugerencia y textos distintos reciban sugerencias distintas, evitando colisiones accidentales.

## Capabilities

### New Capabilities
- `auto-pseudonym-generation`: Core logic to generate and track sequential pseudonyms per category.

### Modified Capabilities
- `excel-workflow`: The exported Excel will now come with pre-filled pseudonyms for new detections.
- `cli-workflow`: The CLI interactive review will suggest automatic pseudonyms.
- `gui-workflow`: The GUI detection process will pre-populate the pseudonym column in the generated Excel.

## Impact

- **Code**: `anonymizer/mapping.py` will likely house the generation logic. `anonymizer/cli.py` and `anonymizer/gui.py` will be updated to use it.
- **UX**: Significant reduction in manual typing during the vetting phase.
- **Data**: No changes to the database schema or Excel structure, just the initial values of the `Pseudonimo` column.
