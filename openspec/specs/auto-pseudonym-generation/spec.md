# auto-pseudonym-generation Specification

## Purpose
Establecer la lógica de generación automática de pseudónimos secuenciales y por categoría para reducir la carga de entrada manual de datos por parte del usuario.

## Requirements
### Requirement: Category-based sequential generation
The system MUST generate pseudonyms following the pattern `{Prefix}{Number}` where Prefix is derived from the entity type.

#### Scenario: Assigning a new person
- **WHEN** a new entity of type `PERSONA` is processed
- **THEN** the first occurrence receives `Persona1`, the second `Persona2`, and so on.

#### Scenario: Cross-document consistency
- **WHEN** the same original text appears multiple times in the same session
- **THEN** it MUST always receive the same auto-pseudonym suggestion to maintain document coherence.

### Requirement: User control over suggestions
The system MUST treat automatically generated pseudonyms as suggestions that can be modified or overridden by the user.

#### Scenario: Overriding a suggestion in Excel
- **WHEN** the user changes `Persona1` to `Director` in the mapping Excel
- **THEN** the system MUST use `Director` for the anonymization, ignoring the original suggestion.
