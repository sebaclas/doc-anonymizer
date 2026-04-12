## ADDED Requirements

### Requirement: Detection context capture
The system MUST capture a surrounding text window for every detected entity to provide operational context. This window SHALL consist of up to 5 words before the match and 5 words after the match. The captured context MUST be stored as metadata with the entity detection.

#### Scenario: Extracting context for a name
- **WHEN** "Juan Perez" is detected in "El ingeniero Juan Perez es el líder."
- **THEN** the system SHALL store a context string similar to "... El ingeniero [Juan Perez] es el líder ..."
