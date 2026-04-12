## Why

Some entities detected by regex are incorrectly labeled as "NER" in the Excel mapping file when using the GUI, making it difficult to verify detection quality. Additionally, the column order for "Type" and "Pseudonym" differs between the mapping Excel and the master database Excel, leading to confusion and potential data corruption during manual or automated syncing.

## What Changes

- **Correct Metadata Preservation**: The GUI detection thread will now use the actual `source` property of the `Entity` object (e.g., "regex", "ner", "known") instead of hardcoding "NER" for non-database hits.
- **Normalized Column Order**: The column order in the interactive Excel mapping file will be updated to match the master database's logic where applicable, or at least standardized to prevent accidental swaps. Specifically, the "Type" and "Pseudonym" columns will be aligned across both templates to [Original, Pseudonimo, Tipo, ...].
- **Default Action for Regex**: The GUI will now automatically set the "Action" to "s" (accept) for high-confidence regex matches, matching the behavior of the CLI.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `excel-workflow`: Update the required column order for the interaction mapping Excel to align with the database schema and ensure "Origen" metadata is correctly populated from all detection sources.
- `entity-detection`: Ensure the `source` metadata is consistently passed and surfaced through all UI layers without being overwritten by default labels.

## Impact

- `anonymizer/gui.py`: The `_detection_thread` logic for row generation and `origen` assignment.
- `anonymizer/mapping.py`: The `save_extended_excel` and `load_extended_data` functions to reflect the new column order.
- `anonymizer/known_entities.py`: Verification of compatibility with the updated mapping format.
- `anonymizer/cli.py`: The `detect` command to ensure consistency with GUI changes.
