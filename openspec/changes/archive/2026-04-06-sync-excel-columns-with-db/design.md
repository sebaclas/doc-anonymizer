## Context

El Excel de detecciones (`save_extended_excel`) genera 6 columnas: Original, Tipo, Pseudónimo, Acción, Guardar DB, Origen. La DB Maestra (`to_excel`) genera 5 columnas: Original, Pseudónimo, Tipo, Aliases, Modo. Ambos Excel representan entidades pero con esquemas incompatibles. Al marcar "Guardar DB = s" en el Excel de detecciones, se crea un `KnownEntity` sin aliases ni modo de coincidencia, requiriendo edición posterior en la DB Maestra.

## Goals / Non-Goals

**Goals:**
- Agregar columnas "Aliases" y "Modo" al Excel de detecciones manteniendo retrocompatibilidad.
- Al guardar entidad a DB desde el Excel de detecciones, incluir aliases y modo si fueron especificados.
- Valores por defecto si el usuario no llena los campos: aliases = vacío, modo = "palabra".
- Actualizar la hoja de instrucciones para documentar las nuevas columnas.

**Non-Goals:**
- No cambiar el formato ni las columnas del Excel de la DB Maestra (`to_excel` / `from_excel`).
- No modificar la estructura interna de `KnownEntity`.
- No cambiar la GUI ni el CLI más allá del paso de guardado a DB.

## Decisions

**Decision 1: Posición de las nuevas columnas.**
Se agregan al final: columnas 7 (Aliases) y 8 (Modo), después de las 6 existentes.
*Rationale:* Mantiene retrocompatibilidad total. Excels existentes (sin estas columnas) se leen correctamente porque `load_extended_data` verifica la longitud del row antes de acceder a columnas opcionales.

**Decision 2: Formato de Aliases en Excel.**
Se usa el mismo formato que en la DB Maestra: texto libre separado por comas.
*Rationale:* Consistencia con el flujo existente de `from_excel` que ya parsea "alias1, alias2" con `split(",")`.

**Decision 3: Valores por defecto.**
- Aliases: cadena vacía (sin aliases)
- Modo: "palabra" (match por word-boundary, más seguro contra falsos positivos)
*Rationale:* Consiste con el default de `KnownEntity.match_mode = "palabra"`.

## Risks / Trade-offs

- [Riesgo] Usuarios avanzados podrían confundir la columna "Modo" sin explicación suficiente.
  → Mitigación: La hoja de instrucciones documenta los valores posibles ("palabra" vs "substring") con ejemplos.
- [Riesgo] Excels con las nuevas columnas abiertos por versiones anteriores del software ignorarán las columnas.
  → Mitigación: Esto es un comportamiento aceptable y no destructivo.
