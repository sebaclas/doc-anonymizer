## Context

Currently, any entity detected that does not exist in the `master_database.xlsx` is assigned an empty string as a pseudonym. This forces the user to manually enter a pseudonym for every new entity in the generated Excel or during the CLI interactive review. This design introduces a mechanism to automatically suggest sequential pseudonyms based on the entity category.

## Goals / Non-Goals

**Goals:**
- Automatically fill the `Pseudonimo` field for new entities with a **suggestion** at the moment of Excel export.
- Allow the user to review, edit, or delete these suggestions in the Excel file before application.
- Ensure pseudonyms are consistent for the same entity text within a document *by default*.
- Ensure pseudonyms are unique within the document processing session *by default*.
- Provide descriptive prefixes based on the entity type (e.g., Persona, Org, Lugar).

**Non-Goals:**
- Overriding manual edits in the Excel file.
- Automatic persistence to the Master Database without user consent (Accion='s' and GuardarDB='s').

## Decisions

### 1. Centralized Generation Logic
A new `AutoPseudonymGenerator` class will be added to `anonymizer/mapping.py`.
- **Properties**: A dictionary of counters indexed by category prefix.
- **Methods**: `get_pseudonym(original_text, entity_type)` which returns the next available pseudonym or a previously assigned one for that text.

### 2. Category Map
The generator will use the following prefix mapping:
- `PERSONA` / `PERSON` -> `Persona`
- `ORGANIZACIÓN` / `ORG` -> `Org`
- `LUGAR` / `LOC` / `LOCATION` -> `Lugar`
- `EMAIL` -> `Email`
- `TELÉFONO` / `PHONE` -> `Tel`
- `DNI/NIE` / `ID_NUMBER` -> `Id`
- Default -> `Ent`

### 3. Integration Points
- **build_mapping()**: Will now accept an optional `AutoPseudonymGenerator` instance to fill missing values.
- **CLI (`cli.py`)**: The `run` command will use the generator to provide defaults for `Prompt.ask`.
- **Excel Export**: Both CLI `detect` and GUI `_detection_thread` will instantiate a generator before building the `data_rows` list for `save_extended_excel`.

## Risks / Trade-offs

- **[Risk]** Name collisions if a real entity's name matches a generated pattern (e.g., a company actually named "Org 1").
  - **→ Mitigation**: The probability is low. Users can always change the suggested value in the Excel file. We will use `PrefixNo` (e.g., `Persona1`) without spaces to further reduce collision risk.
- **[Risk]** Confusion on which entities were auto-filled vs. manual.
  - **→ Mitigation**: The `Origen` column already indicates if it was `NER` or `REGEX`, and the `Accion` column will be pre-filled as `s` for these suggestions, signaling they are ready to be applied unless modified.
