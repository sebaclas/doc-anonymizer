## Context

El Excel de detecciones (`save_extended_excel`) genera 6 columnas: Original, Tipo, Pseudónimo, Acción, Guardar DB, Origen. La DB Maestra (`to_excel`) genera 5 columnas: Original, Pseudónimo, Tipo, Aliases, Modo. Ambos representan entidades pero con esquemas incompatibles.

Al marcar "Guardar DB = s" en el Excel de detecciones, `gui.py` y `cli.py` crean un `KnownEntity` pasando solo `original`, `pseudonym` y `entity_type` — sin aliases ni modo de coincidencia (se usan defaults: aliases=[], match_mode="palabra"). El usuario pierde la oportunidad de definir esos campos en el momento de la detección.

Referencia del código actual:
- `mapping.py:112-154` — `save_extended_excel` escribe 6 columnas
- `mapping.py:157-187` — `load_extended_data` lee 5 columnas (original, pseudo, accion, guardar_db, tipo)
- `known_entities.py:14-19` — `KnownEntity` tiene 5 campos: original, pseudonym, entity_type, aliases, match_mode
- `gui.py:223-233` — `_apply_thread` crea `KnownEntity` sin aliases ni match_mode

## Goals / Non-Goals

**Goals:**
- Agregar columnas "Aliases" (col 7) y "Modo" (col 8) al Excel de detecciones.
- Mantener retrocompatibilidad total: Excels existentes (6 columnas) se leen sin error.
- Al guardar entidad a DB, incluir aliases y modo si fueron especificados por el usuario.
- Valores por defecto: aliases = vacío, modo = "palabra".
- Actualizar la hoja de instrucciones con documentación de las nuevas columnas.

**Non-Goals:**
- No cambiar el formato del Excel de la DB Maestra (`to_excel` / `from_excel` en `known_entities.py`).
- No modificar la estructura interna de `KnownEntity`.
- No cambiar la GUI más allá del paso de guardado a DB.

## Decisions

**Decision 1: Posición de las nuevas columnas.**
Se agregan al final del Excel de detecciones: columna 7 (Aliases) y columna 8 (Modo), después de las 6 existentes.
*Rationale:* Mantiene retrocompatibilidad total. `load_extended_data` verifica `len(row)` antes de acceder a columnas opcionales. Los Excels generados por versiones anteriores no tienen esas columnas y se leen normalmente.

**Decision 2: Formato de Aliases.**
Texto libre separado por comas, idéntico al formato de la DB Maestra.
*Rationale:* Consistencia con `from_excel` en `known_entities.py` (L159) que ya parsea `"alias1, alias2"` con `split(",")`.

**Decision 3: Valores por defecto.**
- Aliases: cadena vacía (sin aliases adicionales)
- Modo: "palabra" (match por word-boundary, más seguro contra falsos positivos)
*Rationale:* Consistente con `KnownEntity.match_mode = "palabra"` (L19).

**Decision 4: Color visual de columnas nuevas.**
Las columnas Aliases y Modo usan el mismo header style que las demás (D5E8F0 bold). No se colorean las celdas de datos (solo las filas con origen=DB siguen en verde).

## Risks / Trade-offs

- [Riesgo] Usuarios podrían confundir la columna "Modo" sin explicación.
  → Mitigación: La hoja de instrucciones ya documenta los valores posibles ("palabra" vs "substring") con ejemplos (L97-99).
- [Riesgo] Excels con 8 columnas abiertos por versiones anteriores del software ignoran columnas 7 y 8.
  → Mitigación: Comportamiento aceptable y no destructivo. Los datos de las 6 primeras columnas se leen correctamente.
