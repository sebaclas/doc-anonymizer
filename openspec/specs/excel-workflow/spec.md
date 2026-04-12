# excel-workflow Specification

## Purpose
Define the interaction model for vetting entity detections using Excel as an offline platform, ensuring data consistency and streamlined manual review.
## Requirements
### Requirement: Generate interactive Excel artifact
The system MUST export a well-formatted `.xlsx` file during the detection step allowing offline entity vetting, extending the current json capabilities. The exported rows MUST be deduplicated by `(text, type)` so that each unique entity appears exactly once to minimize user workload. The column order MUST match the Master Database schema where possible (Original, Contexto, Pseudonimo, Tipo) to prevent data corruption during manual syncing. For entities not matching the Master Database, the system SHALL pre-fill the `Pseudonimo` column with an automatically generated sequential value based on the entity type. These automatic values are **suggestions** only; the user SHALL have the final word and can modify, delete, or ignore them within the Excel file.

#### Scenario: Exporting a unified detection grid with auto-pseudonyms
- **WHEN** user commands detection with excel output flag/method
- **THEN** an `.xlsx` workbook is created where each unique (text, type) pair appears as only a single row.
- **AND THEN** the columns are exactly in this order: Original, Contexto, Pseudonimo, Tipo, Accion, Guardar DB, Origen, Aliases, Modo.
- **AND THEN** any entity not found in the DB SHALL have a suggested pseudonym (e.g., "Persona1") in the `Pseudonimo` column.

### Requirement: Highlight database entities
The system MUST visually distinguish recognized parameters from generic untrusted extractions.

#### Scenario: Metadata preservation for all sources
- **WHEN** an extracted entity is processed for the excel export
- **THEN** its corresponding row `Origen` column MUST hold the actual detection source ("DB", "REGEX" or "NER") correctly.
- **AND THEN** its corresponding row is painted in light green inside the exported `.xlsx` file if and only if `Origen` is "DB".

### Requirement: Excel Application phase
The system MUST be able to apply pseudonym mapping reading off the exported excel correctly.

#### Scenario: Mapping user intents 
- **WHEN** user provides the filled excel to `anonymize apply`
- **THEN** system evaluates the `Accion` column executing the `s`, `n` or `e` procedures accordingly instead of the standard terminal input

### Requirement: Restricted Auto-Approval in Excel
The system SHALL only set the default `Accion` to "s" (apply) for entities that have an exact match in the Known Entities Database. All other entities (NER, Regex) MUST have an empty or neutral default action, requiring explicit user approval.

#### Scenario: Exporting a detection grid with manual approval requirement
- **WHEN** user commands detection with excel output
- **THEN** database hits SHALL have `Accion` set to "s".
- **AND THEN** NER and Regex detections SHALL have an empty `Accion` column, even if they have suggested pseudonyms.

