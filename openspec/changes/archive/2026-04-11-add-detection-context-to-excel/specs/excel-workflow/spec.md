## MODIFIED Requirements

### Requirement: Generate interactive Excel artifact
The system MUST export a well-formatted `.xlsx` file during the detection step allowing offline entity vetting, extending the current json capabilities. The exported rows MUST be deduplicated by `(text, type)` so that each unique entity appears exactly once to minimize user workload. The column order MUST match the Master Database schema where possible (Original, Contexto, Pseudonimo, Tipo) to prevent data corruption during manual syncing.

#### Scenario: Exporting a unified detection grid
- **WHEN** user commands detection with excel output flag/method
- **THEN** an `.xlsx` workbook is created where each unique (text, type) pair appears as only a single row.
- **AND THEN** the columns are exactly in this order: Original, Contexto, Pseudonimo, Tipo, Accion, Guardar DB, Origen, Aliases, Modo.
