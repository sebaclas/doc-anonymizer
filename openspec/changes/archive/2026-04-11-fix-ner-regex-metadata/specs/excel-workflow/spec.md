## MODIFIED Requirements

### Requirement: Generate interactive Excel artifact
The system MUST export a well-formatted `.xlsx` file during the detection step allowing offline entity vetting, extending the current json capabilities. The exported rows MUST be deduplicated by `(text, type)` so that each unique entity appears exactly once to minimize user workload. The column order MUST match the Master Database schema where possible (`Original`, `Pseudonimo`, `Tipo`) to prevent data corruption during manual syncing.

#### Scenario: Exporting a unified detection grid
- **WHEN** user commands detection with excel output flag/method
- **THEN** an `.xlsx` workbook is created where each unique `(text, type)` pair appears as only a single row.
- **AND THEN** the columns are exactly in this order: `Original`, `Pseudonimo`, `Tipo`, `Accion`, `Guardar DB`, `Origen`, `Aliases`, `Modo`.

### Requirement: Highlight database entities
The system MUST visually distinguish recognized parameters from generic untrusted extractions.

#### Scenario: Metadata preservation for all sources
- **WHEN** an extracted entity is processed for the excel export
- **THEN** its corresponding row `Origen` column MUST hold the actual detection source ("DB", "REGEX" or "NER") correctly.
- **AND THEN** its corresponding row is painted in light green inside the exported `.xlsx` file if and only if `Origen` is "DB".
