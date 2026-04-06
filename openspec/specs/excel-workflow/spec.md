## ADDED Requirements

### Requirement: Generate interactive Excel artifact
The system MUST export a well-formatted `.xlsx` file during the detection step allowing offline entity vetting, extending the current json capabilities.

#### Scenario: Exporting a full detection grid
- **WHEN** user commands detection with excel output flag/method
- **THEN** an `.xlsx` workbook is created with exactly these columns: `Original`, `Tipo`, `Pseudonimo`, `Accion`, and `Origen`

### Requirement: Highlight database entities
The system MUST visually distinguish recognized parameters from generic untrusted extractions.

#### Scenario: Green styling for DB hits
- **WHEN** an extracted entity matches an established profile in the user db
- **THEN** its corresponding row is painted in light green inside the exported `.xlsx` file and `Origen` holds "DB"

### Requirement: Excel Application phase
The system MUST be able to apply pseudonym mapping reading off the exported excel correctly.

#### Scenario: Mapping user intents 
- **WHEN** user provides the filled excel to `anonymize apply`
- **THEN** system evaluates the `Accion` column executing the `s`, `n` or `e` procedures accordingly instead of the standard terminal input
