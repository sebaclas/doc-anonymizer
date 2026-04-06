## ADDED Requirements

### Requirement: CLI commands and options
The CLI MUST expose `run`, `detect`, `apply` and `db` commands using Typer framework.

#### Scenario: Running anonymization with full execution
- **WHEN** user executes `anonymize run <file>`
- **THEN** system processes the document natively, performs entity extraction and shows interactive prompts for unresolved entries

#### Scenario: Detecting entities only
- **WHEN** user executes `anonymize detect <file>`
- **THEN** system prints or outputs recognized entities without modifying documents

#### Scenario: Running with no NER
- **WHEN** user passes `--no-ner`
- **THEN** system skips the spaCy detection step and only uses regex rules

### Requirement: Expose DB management
The CLI MUST provide options to list, add, remove, and export/import the known entities database.

#### Scenario: Exporting local DB
- **WHEN** user invokes `anonymize db export`
- **THEN** system produces an Excel file for manual tweaking
