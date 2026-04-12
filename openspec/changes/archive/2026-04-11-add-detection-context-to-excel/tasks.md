## 1. Data Model and Core Logic

- [x] 1.1 Add `context` string field to `Entity` dataclass in `anonymizer/models.py`.
- [x] 1.2 Implement `_get_context(text, start, end, window=5)` helper in `anonymizer/detectors/detector.py`.
- [x] 1.3 Update `detect_all`, `_detect_known` and regex/ner modules to populate the context for every detection.

## 2. Excel Infrastructure

- [x] 2.1 Update `save_extended_excel` in `anonymizer/mapping.py` to include the "Contexto" column at index 2 (between Original and Pseudonimo).
- [x] 2.2 Update `load_extended_data` in `anonymizer/mapping.py` to correctly handle the shifted columns when importing data back.

## 3. UI and CLI Integration

- [x] 3.1 Modify `anonymizer/gui.py` (`_detection_thread`) to pass the entity's context to the Excel row dictionary.
- [x] 3.2 Modify `anonymizer/cli.py` (`detect` command) to include the context in the interactive Excel generation.

## 4. Verification

- [x] 4.1 Validate that the Excel file opens correctly and the "Contexto" column contains the expected text with `[]` around the match.
- [x] 4.2 Verify that applying a mapping from an Excel with the new column still works as expected.
