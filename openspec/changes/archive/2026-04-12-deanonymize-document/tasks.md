## 1. Sidecar Writing (replacer.py)

- [x] 1.1 Define the sidecar JSON schema: `{schema_version, source_document, replacements: [{original, pseudonym, match_mode}]}`
- [x] 1.2 Add `_write_reversal_sidecar(output_path, source_document, mapping, modes)` helper that collects the applied substitution pairs (deduplicated) and writes `<output_path>.reversal.json`
- [x] 1.3 Call `_write_reversal_sidecar` at the end of `anonymize_docx` (with `write_reversal=True` default and opt-out param)
- [x] 1.4 Call `_write_reversal_sidecar` at the end of `anonymize_pdf` (same pattern)
- [x] 1.5 Write unit tests for `_write_reversal_sidecar`: correct JSON structure, deduplication, opt-out suppresses file creation

## 2. Sidecar Loader

- [x] 2.1 Add `load_reversal_sidecar(path: str | Path) -> dict[str, str]` in `replacer.py` (or a new `reversal.py` if file grows large) that reads the JSON and returns `{pseudonym: original}`
- [x] 2.2 Raise `FileNotFoundError` with an informative message if the sidecar path does not exist
- [x] 2.3 Log a `WARNING` if two entries share the same pseudonym (collision) and use last-entry-wins
- [x] 2.4 Write unit tests: valid sidecar returns correct dict, missing file raises error, collisions log warning and return last value

## 3. De-anonymization Functions (replacer.py)

- [x] 3.1 Add `deanonymize_docx(input_path, output_path, reversal_path)` that calls `load_reversal_sidecar` and passes `{pseudo: original}` with `"substring"` mode for all keys to `_deep_replace_xml`
- [x] 3.2 Add `deanonymize_pdf(input_path, output_path, reversal_path)` mirroring `anonymize_pdf` but using the loaded reverse mapping
- [x] 3.3 Write unit tests: successful round-trip for DOCX (anonymize → deanonymize → assert original text), successful round-trip for PDF, empty sidecar produces unchanged output

## 4. CLI Subcommand (cli.py)

- [x] 4.1 Add `deanonymize` subcommand with positional args `<input>` `<output>` and optional `--reversal <path>`
- [x] 4.2 Auto-detect reversal path as `<input>.reversal.json` when `--reversal` is omitted
- [x] 4.3 Validate: input exists, extension is `.docx` or `.pdf`, sidecar exists (or `--reversal` provided); print clear errors and exit non-zero on failures
- [x] 4.4 Dispatch to `deanonymize_docx` or `deanonymize_pdf` and print success confirmation
- [x] 4.5 Write CLI integration tests: DOCX round-trip, PDF round-trip, missing sidecar error, unsupported extension error

## 5. GUI Action (gui.py)

- [x] 5.1 Add "Revertir anonimización" button in the document processing section
- [x] 5.2 Implement click handler: open file picker for anonymized document, auto-derive sidecar path, open save dialog for output path
- [x] 5.3 If sidecar is missing, show error dialog: "Este archivo no tiene un archivo de reversión asociado. Solo se pueden revertir documentos anonimizados con esta herramienta."
- [x] 5.4 Run de-anonymization in a background thread (reuse existing threading pattern from `gui.py`), show success or error notification on completion

## 6. Regression & Integration Tests

- [x] 6.1 Add end-to-end round-trip regression test: anonymize fixture DOCX → confirm sidecar exists → deanonymize → assert text matches original fixture
- [x] 6.2 Add end-to-end round-trip regression test for PDF (text-level comparison)
- [x] 6.3 Run full test suite and confirm all existing anonymization tests remain green
