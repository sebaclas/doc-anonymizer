## MODIFIED Requirements

### Requirement: Generate interactive Excel artifact
The system MUST export a well-formatted `.xlsx` file during the detection step allowing offline entity vetting, extending the current json capabilities. The exported rows MUST be deduplicated by `(text, type)` so that each unique entity appears exactly once to minimize user workload. The column order MUST match the Master Database schema where possible (Original, Contexto, Pseudonimo, Tipo) to prevent data corruption during manual syncing. For entities not matching the Master Database, the system SHALL pre-fill the `Pseudonimo` column with an automatically generated sequential value based on the entity type. These automatic values are **suggestions** only; the user SHALL have the final word and can modify, delete, or ignore them within the Excel file.

#### Scenario: Exporting a unified detection grid with auto-pseudonyms
- **WHEN** user commands detection with excel output flag/method
- **THEN** an `.xlsx` workbook is created where each unique (text, type) pair appears as only a single row.
- **AND THEN** the columns are exactly in this order: Original, Contexto, Pseudonimo, Tipo, Accion, Guardar DB, Origen, Aliases, Modo.
- **AND THEN** any entity not found in the DB SHALL have a suggested pseudonym (e.g., "Persona1") in the `Pseudonimo` column.
