## Why

Currently, if the same entity (e.g., a person's name) appears multiple times in a document, it is detected multiple times and written as multiple duplicate rows in the generated review Excel file. This forces the user to review and set pseudonyms for the exact same entity repeatedly, frustrating the user and creating an inefficient workflow. We need to deduplicate entities based on their text and type before generating the Excel file so that each unique entity only requires a single assignment.

## What Changes

- Deduplicate the list of detected entities by grouping them by their `text` and `entity_type` before passing them to the Excel generation.
- Ensure that the resulting Excel file contains only one row per unique entity.
- The downstream anonymization process will use this deduplicated mapping, which works correctly because it applies replacements by replacing matching string occurrences in the document.

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `excel-workflow`: The requirement for what gets exported to the Excel file changes from "all detected entity instances" to "only unique detected entities".
- `gui-workflow`: The GUI integration with the Excel file generation should pass deduplicated entities to the export logic.
- `cli-workflow`: The CLI integration with the Excel file generation should also pass deduplicated entities to the export logic.

## Impact

- `anonymizer/gui.py` and `anonymizer/cli.py` (or perhaps `anonymizer/mapping.py` / `anonymizer/detectors/detector.py` depending on the design) will be affected to incorporate the deduplication step.
- The generated Excel mapper will be significantly smaller for documents with repeating entities.
