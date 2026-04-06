# entity-matching Specification

## Purpose
TBD - created by archiving change initial-spec. Update Purpose after archive.
## Requirements
### Requirement: Exact and approximate string matching
The system MUST compare extracted tokens to the `known_entities.json` DB using Exact match or Fuzzy match via `rapidfuzz`.

#### Scenario: Resolving fuzzy acronyms/names
- **WHEN** threshold is >= 85 and similarity checks pass for a localized name variation
- **THEN** system auto-maps or prompts context-specific resolution dynamically

### Requirement: Interactive prompt
System MUST pause and prompt users via `Rich` dialogs for entities unseen in the Local DB.

#### Scenario: Accepting/Rejecting new tokens
- **WHEN** a new entity is discovered
- **THEN** the workflow pauses, expects keyboard input ('s' / 'n' / 'e') and asks for pseudonym provision on 's'

### Requirement: Storage formatting mode
DB MUST save entity mode search options: `palabra` (word-boundary) or `substring`.

#### Scenario: Alias matching with substrings
- **WHEN** an entry is saved with `substring` mode
- **THEN** the replacer mechanism substitutes it even if appended within other strings

