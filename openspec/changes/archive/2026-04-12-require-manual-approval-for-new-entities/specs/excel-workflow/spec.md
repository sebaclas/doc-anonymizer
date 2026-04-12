## ADDED Requirements

### Requirement: Restricted Auto-Approval in Excel
The system SHALL only set the default `Accion` to "s" (apply) for entities that have an exact match in the Known Entities Database. All other entities (NER, Regex) MUST have an empty or neutral default action, requiring explicit user approval.

#### Scenario: Exporting a detection grid with manual approval requirement
- **WHEN** user commands detection with excel output
- **THEN** database hits SHALL have `Accion` set to "s".
- **AND THEN** NER and Regex detections SHALL have an empty `Accion` column, even if they have suggested pseudonyms.
