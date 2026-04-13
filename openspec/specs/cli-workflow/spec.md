# cli-workflow Specification

## Purpose
TBD - created by archiving change initial-spec. Update Purpose after archive.
## Requirements
### Requirement: CLI commands and options
The CLI MUST expose `run`, `detect`, `apply` and `db` commands using Typer framework. All commands involving file outputs SHALL respect the new project structure and avoid polluting the root directory.

#### Scenario: Running anonymization with full execution
- **WHEN** user executes `anonymize run <file>`
- **THEN** system processes the document natively, performs entity extraction and shows interactive prompts for unresolved entries.
- **AND THEN** the interactive prompts SHALL suggest an automatically generated pseudonym but MUST NOT auto-approve individual new entities unless they were previously known.

#### Scenario: Detecting entities only
- **WHEN** user executes `anonymize detect <file>`
- **THEN** system prints or outputs recognized entities without modifying documents.
- **AND THEN** if Excel output is requested, new entities SHALL have suggested pseudonyms pre-filled, but the `Accion` column SHALL be empty for non-database detections.

### Requirement: Expose DB management
The CLI MUST provide options to list, add, remove, and export/import the known entities database.

#### Scenario: Exporting local DB
- **WHEN** user invokes `anonymize db export`
- **THEN** system produces an Excel file for manual tweaking

