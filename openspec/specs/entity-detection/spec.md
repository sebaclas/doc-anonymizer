# entity-detection Specification

## Purpose
TBD - created by archiving change initial-spec. Update Purpose after archive.
## Requirements
### Requirement: AI NER Detection
The system MUST detect PERSON, ORGANIZATION, and LOCATION entities using spaCy NER. The active model is determined at runtime as the first available model in the `ner_models` configuration list. The minimum character length for detected entities SHALL be 3 to accommodate common 3-letter organizational acronyms.

#### Scenario: Standard document NER
- **WHEN** processing general unstructured text containing 3-letter acronyms like 'BRT' or 'SAP'
- **THEN** system extracts recognized named entities using the first available model in the configured list and flags them for checking

#### Scenario: Error message when no model is available
- **WHEN** no model from the `ner_models` list can be loaded
- **THEN** the system raises a descriptive error listing the models it attempted to load, without suggesting specific hardcoded model names

### Requirement: Proactive Database Detection
The system MUST proactively scan for all entries (originals and aliases) stored in the Known Entities Database as part of the detection step. This ensures that established entities are always flagged even if AI models miss them.

#### Scenario: Detecting known short acronyms
- **WHEN** a document contains 'GDP' and this term is defined in the Known Entities DB
- **THEN** the system MUST detect 'GDP' and label its source as 'database' or 'db', even if it is shorter than the standard NER threshold.

### Requirement: Regex extraction module
The system MUST support rigid struct matching for predefined attributes like CUIT, DNI, email, IBAN, CBU via standard regex.

#### Scenario: Identifying structured tokens
- **WHEN** parsing formatted strings like emails or phone numbers
- **THEN** system identifies the exact bounds and extracts them without false positives

### Requirement: Detection context capture
The system MUST capture a surrounding text window for every detected entity to provide operational context. This window SHALL consist of up to 5 words before the match and 5 words after the match. The captured context MUST be stored as metadata with the entity detection.

#### Scenario: Extracting context for a name
- **WHEN** "Juan Perez" is detected in "El ingeniero Juan Perez es el líder."
- **THEN** the system SHALL store a context string similar to "... El ingeniero [Juan Perez] es el líder ..."

