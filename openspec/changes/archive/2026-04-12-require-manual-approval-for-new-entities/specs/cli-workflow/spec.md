## MODIFIED Requirements

### Requirement: CLI commands and options
The CLI MUST expose `run`, `detect`, `apply` and `db` commands using Typer framework.

#### Scenario: Running anonymization with full execution
- **WHEN** user executes `anonymize run <file>`
- **THEN** system processes the document natively, performs entity extraction and shows interactive prompts for unresolved entries.
- **AND THEN** the interactive prompts SHALL suggest an automatically generated pseudonym but MUST NOT auto-approve individual new entities unless they were previously known.

#### Scenario: Detecting entities only
- **WHEN** user executes `anonymize detect <file>`
- **THEN** system prints or outputs recognized entities without modifying documents.
- **AND THEN** if Excel output is requested, new entities SHALL have suggested pseudonyms pre-filled, but the `Accion` column SHALL be empty for non-database detections.
