## ADDED Requirements

### Requirement: Sequential category-based pseudonym generation
The system MUST generate sequential pseudonyms based on the entity type when no manual pseudonym is provided. The format SHALL be `<TypePrefix><SequenceNumber>`.

#### Scenario: Generating pseudonyms for multiple persons
- **WHEN** building a mapping for "Juan Perez" (PERSONA) and "Maria Garcia" (PERSONA)
- **THEN** "Juan Perez" SHALL be assigned "Persona1"
- **AND** "Maria Garcia" SHALL be assigned "Persona2"

### Requirement: Document-level pseudonym consistency
The system MUST ensure that the same original entity text always receives the same pseudonym within a single processing session, even if it appears multiple times.

#### Scenario: Repeated entity detection
- **WHEN** "Empresa Estatal" appears twice in a document and is detected as ORGANIZACIÓN
- **THEN** both occurrences SHALL be mapped to the same generated pseudonym (e.g., "Org1")

### Requirement: Uniqueness across categories
The system MUST ensure that generated pseudonyms are unique within the document, even if different categories share prefixes.

#### Scenario: Multiple categories
- **WHEN** processing PERSONA and ORGANIZACIÓN entities
- **THEN** the system SHALL ensure that "Persona1" and "Org1" are distinct and do not overlap with any manual entries
