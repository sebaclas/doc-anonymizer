## ADDED Requirements

### Requirement: Proactive Database Detection
The system MUST proactively scan for all entries (originals and aliases) stored in the Known Entities Database as part of the detection step. This ensures that established entities are always flagged even if AI models miss them.

#### Scenario: Detecting known short acronyms
- **WHEN** a document contains 'GDP' and this term is defined in the Known Entities DB
- **THEN** the system MUST detect 'GDP' and label its source as 'database' or 'db', even if it is shorter than the standard NER threshold.

## MODIFIED Requirements

### Requirement: AI NER Detection
The system MUST detect PERSON, ORGANIZATION, and LOCATION entities using spaCy's `xx_ent_wiki_sm` model. The minimum character length for detected entities SHALL be 3 to accommodate common 3-letter organizational acronyms.

#### Scenario: Standard document NER
- **WHEN** processing general unstructured text containing 3-letter acronyms like 'BRT' or 'SAP'
- **THEN** system extracts recognized named entities and flags them for checking
