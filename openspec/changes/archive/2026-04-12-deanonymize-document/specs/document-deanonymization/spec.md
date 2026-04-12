## ADDED Requirements

### Requirement: Write reversal sidecar on anonymization
The system SHALL write a `.reversal.json` sidecar file alongside every anonymized output document. The sidecar MUST contain a schema version, the source document filename, and an ordered list of `{original, pseudonym, match_mode}` records for every substitution applied during anonymization.

#### Scenario: Sidecar created alongside anonymized DOCX
- **WHEN** `anonymize_docx` completes successfully for `output.docx`
- **THEN** a file `output.docx.reversal.json` is created in the same directory containing all applied substitution pairs

#### Scenario: Sidecar created alongside anonymized PDF
- **WHEN** `anonymize_pdf` completes successfully for `output.pdf`
- **THEN** a file `output.pdf.reversal.json` is created in the same directory containing all applied substitution pairs

#### Scenario: Sidecar omitted when explicitly suppressed
- **WHEN** `anonymize_docx` or `anonymize_pdf` is called with `write_reversal=False`
- **THEN** no `.reversal.json` file is created

#### Scenario: Sidecar contains no duplicates
- **WHEN** the same (original, pseudonym) pair appears multiple times in the mapping
- **THEN** the sidecar records it only once

### Requirement: Load reversal mapping from sidecar
The system SHALL provide a function `load_reversal_sidecar(path)` that reads a `.reversal.json` file and returns a `{pseudonym: original}` dict built from the stored replacement list, independent of the master database.

#### Scenario: Sidecar loaded successfully
- **WHEN** `load_reversal_sidecar` is called with a valid path
- **THEN** the returned dict maps every stored pseudonym to its original text

#### Scenario: Error on missing sidecar
- **WHEN** `load_reversal_sidecar` is called with a path that does not exist
- **THEN** a clear `FileNotFoundError` is raised with a message indicating the sidecar is missing

#### Scenario: Warning on pseudonym collision within sidecar
- **WHEN** two entries in the sidecar share the same pseudonym but differ in original
- **THEN** the function logs a warning and uses the last entry in list order

### Requirement: De-anonymize DOCX document
The system SHALL provide `deanonymize_docx(input_path, output_path, reversal_path)` that reads the sidecar, builds the reverse mapping, and applies it to the anonymized DOCX using substring match mode for all entries, preserving paragraph and run structure.

#### Scenario: Successful DOCX reversal
- **WHEN** `deanonymize_docx` is called with a valid anonymized DOCX and its sidecar
- **THEN** the output DOCX contains the original entity names in place of pseudonyms

#### Scenario: Unchanged document when sidecar has no entries
- **WHEN** the sidecar `replacements` list is empty
- **THEN** the output DOCX is identical in text content to the input

### Requirement: De-anonymize PDF document
The system SHALL provide `deanonymize_pdf(input_path, output_path, reversal_path)` that reads the sidecar and restores original entity names in a new plain-structural PDF.

#### Scenario: Successful PDF reversal
- **WHEN** `deanonymize_pdf` is called with a valid anonymized PDF and its sidecar
- **THEN** the output PDF contains the original entity names in place of pseudonyms

### Requirement: CLI deanonymize subcommand
The system SHALL expose a `deanonymize` subcommand in the CLI with positional args `<input>` and `<output>` and an optional `--reversal <path>` flag. If `--reversal` is omitted, the CLI MUST auto-detect the sidecar at `<input>.reversal.json`.

#### Scenario: CLI de-anonymizes a DOCX using auto-detected sidecar
- **WHEN** `anonymizer deanonymize input.docx output.docx` is run and `input.docx.reversal.json` exists
- **THEN** `output.docx` is created with pseudonyms replaced by originals and exit code 0

#### Scenario: CLI de-anonymizes using explicit sidecar path
- **WHEN** `anonymizer deanonymize input.docx output.docx --reversal mapping.reversal.json` is run
- **THEN** the specified reversal file is used

#### Scenario: CLI errors when sidecar is missing
- **WHEN** the auto-detected sidecar does not exist and `--reversal` was not provided
- **THEN** the CLI prints a clear error message and exits with a non-zero code

#### Scenario: CLI errors on unsupported format
- **WHEN** the input file is not DOCX or PDF
- **THEN** the CLI prints an error and exits with a non-zero code

### Requirement: GUI de-anonymization action
The system SHALL provide a "Revertir anonimización" button in the GUI. When clicked, the GUI MUST open a file picker for the anonymized document, auto-detect its sidecar, and run de-anonymization in a background thread. If the sidecar is missing, an error dialog MUST explain that the file was not reversible.

#### Scenario: GUI completes de-anonymization with auto-detected sidecar
- **WHEN** the user selects an anonymized document that has a sidecar beside it
- **THEN** the de-anonymized document is saved and a success notification is shown

#### Scenario: GUI shows error when sidecar is absent
- **WHEN** the user selects an anonymized document without a `.reversal.json` sidecar
- **THEN** an error dialog explains the reversal file is missing and no output is created
