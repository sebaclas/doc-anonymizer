## Why

Once a document is anonymized, there is currently no way to reverse the process — meaning pseudonyms cannot be swapped back for original entity names. This blocks workflows where users need to re-inspect or distribute the restored original. The operation must be **document-local and DB-independent**: pseudonyms are not unique keys in the master database (multiple originals can share the same pseudonym), so any reversal strategy that reads from the DB would be ambiguous. The only reliable source of truth is the exact set of substitutions that were applied to each specific document.

## What Changes

- During `anonymize_docx` / `anonymize_pdf`, a **sidecar reversal file** (`<output>.reversal.json`) is written alongside the anonymized document. It captures the ordered list of exact `{original, pseudonym}` pairs that were actually applied to that document.
- A new `deanonymize` operation reads the sidecar file and applies the inverse substitutions directly to the anonymized document, producing the restored original. **No DB access is required.**
- The CLI will gain a `deanonymize` subcommand: `anonymizer deanonymize <anonymized_doc> <output> [--reversal <path>]` (sidecar auto-detected if omitted).
- The GUI will expose a "Revertir anonimización" action that detects the sidecar automatically from the selected file's path.
- The core `replacer` module will be extended with `deanonymize_docx` / `deanonymize_pdf` functions.

## Capabilities

### New Capabilities

- `document-deanonymization`: Capability to reverse an anonymized document back to its original content using a document-local sidecar reversal file, without relying on the master database.

### Modified Capabilities

- `document-processing`: The anonymization functions for DOCX and PDF gain sidecar-writing behaviour, and new reverse-replacement scenarios are added.

## Impact

- `anonymizer/replacer.py` — `anonymize_docx` / `anonymize_pdf` write a `.reversal.json` sidecar; new `deanonymize_docx` / `deanonymize_pdf` functions read it.
- `anonymizer/cli.py` — new `deanonymize` subcommand.
- `anonymizer/gui.py` — new "Revertir anonimización" action.
- No DB schema changes. The sidecar file is the only new artefact on disk.
