## Why

Currently, the Excel mapping file only shows the detected text and its type. Users often need to see the surrounding context (neighboring words) to decide whether a detection is a false positive or needs to be anonymized, especially for ambiguous terms.

## What Changes

- **Detection Context Acquisition**: The detection engine will now capture a window of context (5 words before and 5 words after) for each entity found in the document.
- **Excel Schema Update**: A new "Contexto" column will be added to the interactive Excel mapping file, positioned after the "Original" text.
- **Deduplication Strategy**: When unique entities are collected for the mapping file, the context from the first occurrence in the document will be preserved.
- **GUI & CLI Integration**: Both interfaces will be updated to include this context when generating the Excel file.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `excel-workflow`: Update the Excel template to include a read-only "Contexto" column and ensure the export logic populates it from the detection metadata.
- `entity-detection`: Update the detection process to extract and store surrounding text window for every match found.

## Impact

- `anonymizer/models.py`: Addition of `context` field to `Entity` dataclass.
- `anonymizer/detectors/detector.py`: New logic to extract word-based context using match offsets.
- `anonymizer/mapping.py`: Update `save_extended_excel` to handle the new "Contexto" column.
- `anonymizer/gui.py`: Update row generation in `_detection_thread`.
- `anonymizer/cli.py`: Update `detect` command Excel generation.
