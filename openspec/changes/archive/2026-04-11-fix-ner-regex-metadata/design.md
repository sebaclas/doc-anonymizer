## Context

The current system has an inconsistency between the "Mapping Excel" (used for reviewing detections) and the "Master Database Excel" (the persistent store). 
- Mapping Excel: `[Original, Tipo, Pseudonimo, ...]`
- Master DB: `[Original, Pseudonimo, Tipo, ...]`

This flip causes confusion and data corruption if users manually copy-paste between them or if the system doesn't handle the mapping perfectly. Additionally, the GUI fails to report the correct detection source (NER vs Regex).

## Goals / Non-Goals

**Goals:**
- Harmonize the column order across all system Excels to prevent data swaps.
- Correct the "Origen" column in the Mapping Excel to reflect the actual detection source.
- Improve UX by auto-approving regex detections in the GUI (consistent with CLI).

**Non-Goals:**
- Changing the schema of the `custom_patterns.json`.
- Implementing a full-blown database engine (keeping Excel).

## Decisions

### 1. Unified Column Order
We will adopt the Master Database's order for the first three columns in all exported Excels.
- **New Order:** `[Original, Pseudonimo, Tipo, Accion, Guardar DB, Origen, Aliases, Modo]`
- **Rationale:** By putting `Pseudonimo` before `Tipo`, we match the established Master Database schema. This allows the first 3 columns to be identical across both file types, facilitating easier manual verification and reliable programmatic swapping.

### 2. Explicit Source Mapping in GUI
The `_detection_thread` in `gui.py` will be modified to use `ent.source.upper()`.
- **Rationale:** The `Entity` object already carries the correct source ("ner", "regex", "known"). Hardcoding "NER" was a regression from early development stages.

## Risks / Trade-offs

- **[Risk] Migration of In-progress Mappings** → Existing mapping files generated with the old column order will fail to load correctly with the new code.
- **[Mitigation]** Accept the risk, Priority is establishing the new standard. Since mapping files are ephemeral per-document, the risk is low.
