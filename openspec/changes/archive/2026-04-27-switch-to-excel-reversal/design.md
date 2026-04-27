## Context

The system currently uses a JSON sidecar to store the mapping for de-anonymization. This creates a disconnect from the Excel mapping file, which is the primary interface for users. We are moving towards a single source of truth: the Excel mapping file.

## Goals / Non-Goals

**Goals:**
- Eliminate the generation of `.reversal.json` sidecar files.
- Enable restoration of documents using an Excel mapping file as the input for the reverse mapping (`pseudonym -> original`).
- Update CLI and GUI to support the Excel-based restoration workflow.

**Non-Goals:**
- Backwards compatibility with existing `.reversal.json` files.
- Automated tracking of which Excel belongs to which document (user provided).

## Decisions

### 1. Reverse Mapping Extraction in `mapping.py`
We will add a new function `load_reverse_mapping(excel_path)` to `anonymizer/mapping.py`. This function will:
- Parse the Excel (handling both standard and extended formats).
- Build a dictionary where `key = pseudonym` and `value = original_text`.
- Handle collisions (same pseudonym for multiple originals) by letting the last one in the file win, consistent with previous behavior.

### 2. Streamlining `replacer.py`
- Remove the `_write_reversal_sidecar` function.
- Remove the `write_reversal` parameter from `anonymize_docx` and `anonymize_pdf`.
- Update `deanonymize_docx` and `deanonymize_pdf` to accept a `mapping_dict` directly or call the new Excel loader.

### 3. CLI Subcommand `restore`
The `restore` command will be updated:
- Remove the argument for a sidecar path.
- Add a required `--mapping` (or `-m`) option to point to the Excel file.

### 4. GUI Restoration Flow
The "Restaurar" action in the GUI will now prompt for two files:
1. The anonymized document.
2. The corresponding Excel mapping file.

## Risks / Trade-offs

- **[Risk]** Loss of Excel file renders document irreversible. -> **Mitigation**: User is informed that the Excel is the unique key for restoration. Add a warning un Manual.md and mini-manual and README.md
- **[Risk]** Excel file format changes or manual edits break parsing. -> **Mitigation**: Use existing robust parsing logic from `mapping.py` which handles format variations.
- **[Risk]** Case sensitivity loss in reversal. -> **Mitigation**: As discussed, if multiple originals map to one pseudonym, the reversal is lossy regarding casing. This is an existing limitation of the string-replacement approach.
