## MODIFIED Requirements

### Requirement: Generate interactive Excel artifact
The system MUST export a well-formatted `.xlsx` file during the detection step allowing offline entity vetting, extending the current json capabilities. The exported rows MUST be deduplicated by `(text, type)` so that each unique entity appears exactly once to minimize user workload.

#### Scenario: Exporting a deduplicated detection grid
- **WHEN** user commands detection with excel output flag/method and the document contains multiple identical occurrences of an entity
- **THEN** an `.xlsx` workbook is created where each unique `(text, type)` pair appears as only a single row, minimizing repeated assignments.
- **AND THEN** the columns are exactly: `Original`, `Tipo`, `Pseudonimo`, `Accion`, and `Origen` (plus any internal UI state elements like `guardar_db` as required).
