## MODIFIED Requirements

### Requirement: AI NER Detection
The system MUST detect PERSON, ORGANIZATION, and LOCATION entities using spaCy NER. The active model is determined at runtime as the first available model in the `ner_models` configuration list. The minimum character length for detected entities SHALL be 3 to accommodate common 3-letter organizational acronyms.

#### Scenario: Standard document NER
- **WHEN** processing general unstructured text containing 3-letter acronyms like 'BRT' or 'SAP'
- **THEN** system extracts recognized named entities using the first available model in the configured list and flags them for checking

#### Scenario: Error message when no model is available
- **WHEN** no model from the `ner_models` list can be loaded
- **THEN** the system raises a descriptive error listing the models it attempted to load, without suggesting specific hardcoded model names
