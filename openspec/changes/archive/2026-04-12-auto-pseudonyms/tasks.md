## 1. Core Implementation

- [x] 1.1 Implement `AutoPseudonymGenerator` class in `anonymizer/mapping.py` with category-based prefixes.
- [x] 1.2 Pass the generator instance to `build_mapping` logic.
- [x] 1.3 Add unit tests in `tests/test_mapping_auto.py` to verify sequentiality and uniqueness.

## 2. CLI Updates

- [x] 2.1 Update `anonymize run` interactives to use auto-pseudonyms as defaults for Prompt.ask.
- [x] 2.2 Update `anonymize detect --output mapping.xlsx` to pre-populate the Pseudonimo column.
- [x] 2.3 Verify CLI help and command execution.

## 3. GUI Updates

- [x] 3.1 Update `_detection_thread` in `anonymizer/gui.py` to use `AutoPseudonymGenerator` for new detections.
- [x] 3.2 Pre-set `accion="s"` when an auto-pseudonym is assigned in GUI Excel export.
- [x] 3.3 Verify GUI flow: Detect -> Review Excel (with suggestions) -> Apply.

## 4. Documentation & Verification

- [x] 4.1 Update `MANUAL.md` (if necessary) to mention automatic pseudonym suggestions.
- [x] 4.2 Final audit of the code changes.
