## 1. Core Mapping Logic

- [x] 1.1 Implement `load_reverse_mapping(excel_path)` in `anonymizer/mapping.py` to extract `{pseudonym: original}` from both standard and extended Excel formats.
- [x] 1.2 Verify that the loader handles collisions by taking the last occurrence.

## 2. Document Replacer Updates

- [x] 2.1 Remove `_write_reversal_sidecar` and `load_reversal_sidecar` from `anonymizer/replacer.py`.
- [x] 2.2 Update `anonymize_docx` and `anonymize_pdf` to remove sidecar generation logic and cleanup parameters.
- [x] 2.3 Update `deanonymize_docx` and `deanonymize_pdf` to accept an Excel path and use the new mapping loader.

## 3. CLI Interface

- [x] 3.1 Update the `deanonymize` command in `anonymizer/cli.py` to make `--mapping` / `-m` a required argument.
- [x] 3.2 Remove the logic for auto-detecting `.reversal.json` files in the command.
- [x] 3.3 Update help strings and error messages to reflect the requirement of an Excel file.

## 4. GUI Restoration Flow

- [x] 4.1 Update the restoration button logic in `anonymizer/gui.py` to prompt the user for the Excel mapping file.
- [x] 4.2 Update the de-anonymization thread to pass the Excel path to the replacer.

## 5. Cleanup

- [x] 5.1 Remove sidecar-related diagnostic or logging messages.
- [x] 5.2 Delete any existing `.reversal.json` files in the `sample_docs` directory to avoid confusion.
