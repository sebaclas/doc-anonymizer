# document-deanonymization Specification (Delta)

## REMOVED Requirements

### Requirement: Write reversal sidecar on anonymization
**Reason**: Replaced by direct use of Excel mapping files to unify the workflow and eliminate redundant sidecar files.
**Migration**: Use the existing `.xlsx` mapping file generated during anonymization.

### Requirement: Load reversal mapping from sidecar
**Reason**: Replaced by new Excel-based loading logic.
**Migration**: Path to `.reversal.json` is no longer supported.

## MODIFIED Requirements

### Requirement: De-anonymize DOCX document
The system SHALL provide `deanonymize_docx(input_path, output_path, mapping_path)` that reads an Excel mapping file, builds the reverse mapping (`pseudonym -> original`), and applies it to the anonymized DOCX using substring match mode for all entries.

#### Scenario: Successful DOCX reversal from Excel
- **WHEN** `deanonymize_docx` is called with a valid anonymized DOCX and its mapping Excel
- **THEN** the output DOCX contains the original entity names in place of pseudonyms

### Requirement: De-anonymize PDF document
The system SHALL provide `deanonymize_pdf(input_path, output_path, mapping_path)` that reads the mapping Excel and restores original entity names in a new plain-structural PDF.

#### Scenario: Successful PDF reversal from Excel
- **WHEN** `deanonymize_pdf` is called with a valid anonymized PDF and its mapping Excel
- **THEN** the output PDF contains the original entity names in place of pseudonyms

### Requirement: CLI deanonymize subcommand
The system SHALL expose a `deanonymize` subcommand in the CLI with positional args `<input>` and `<output>` and a REQUIRED `--mapping <path>` (or `-m`) flag to provide the Excel mapping file.

#### Scenario: CLI de-anonymizes a DOCX using Excel mapping
- **WHEN** `anonymizer deanonymize input.docx output.docx --mapping mapeo.xlsx` is run
- **THEN** `output.docx` is created with pseudonyms replaced by originals and exit code 0

#### Scenario: CLI errors when mapping file is missing or invalid
- **WHEN** the `--mapping` file does not exist or is not a valid Excel
- **THEN** the CLI prints a clear error message and exits with a non-zero code

### Requirement: GUI de-anonymization action
The system SHALL provide a "Restaurar" button in the GUI. When clicked, the GUI MUST open a dialog prompting for both the anonymized document AND its corresponding Excel mapping file.

#### Scenario: GUI completes de-anonymization with selected Excel
- **WHEN** the user selects an anonymized document and its mapping Excel
- **THEN** the restored document is saved and a success notification is shown
