# entity-detection Specification

## Purpose
TBD - created by archiving change initial-spec. Update Purpose after archive.
## Requirements
### Requirement: AI NER Detection
The system MUST detect PERSON, ORGANIZATION, and LOCATION entities using spaCy's `xx_ent_wiki_sm` model.

#### Scenario: Standard document NER
- **WHEN** processing general unstructured text
- **THEN** system extracts recognized named entities and flags them for checking

### Requirement: Regex extraction module
The system MUST support rigid struct matching for predefined attributes like CUIT, DNI, email, IBAN, CBU via standard regex.

#### Scenario: Identifying structured tokens
- **WHEN** parsing formatted strings like emails or phone numbers
- **THEN** system identifies the exact bounds and extracts them without false positives

