## Why

The current de-anonymization workflow relies on a `.reversal.json` sidecar file that is automatically generated but often disconnected from the user's mental model. By switching to the Excel mapping file as the sole source of truth for restoration, we unify the workflow, increase transparency, and allow users to directly correct or audit the reversal mapping using tools they are already familiar with.

## What Changes

- **REMOVAL**: Generation of `.reversal.json` sidecar files during the anonymization process.
- **MODIFICATION**: The de-anonymization (restoration) engine will now read the mapping directly from the "Original" and "Pseudonym" columns of the session's Excel file.
- **MODIFICATION**: CLI and GUI restoration commands will now require the user to provide the corresponding Excel mapping file.
- **MODIFICATION**: Removal of sidecar-specific logic and schema versioning.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `document-deanonymization`: Requirement changed to use the Excel mapping file instead of a JSON sidecar for the reversal mapping.

## Impact

- `anonymizer/replacer.py`: Change `anonymize_docx`/`anonymize_pdf` (remove sidecar write) and `deanonymize_docx`/`deanonymize_pdf` (change mapping source).
- `anonymizer/cli.py`: Update `restore` subcommand arguments and logic.
- `anonymizer/gui.py`: Update the de-anonymization flow to prompt for the Excel file.
- `anonymizer/mapping.py`: Add or refine logic to extract a reverse mapping (`pseudonym -> original`) from the Excel format.
