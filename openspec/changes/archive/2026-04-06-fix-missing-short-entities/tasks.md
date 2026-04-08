## 1. Core Logic Updates

- [x] 1.1 In `anonymizer/detectors/ner.py`, change `len(text) < 4` to `len(text) < 3` in `_extract_from_span`.
- [x] 1.2 In `anonymizer/detectors/detector.py`, implement `_detect_known` using regex word-boundary searches for all strings in the Known Entities DB.
- [x] 1.3 Update `detect_all` to take an optional `known_entities` list and call `_detect_known`.
- [x] 1.4 Update the deduplication logic in `detector.py` to prioritize `source='known'` entities.

## 2. Integration

- [x] 2.1 Update `anonymizer/cli.py` to pass the loaded DB entities to `detect_all`.
- [x] 2.2 Update `anonymizer/gui.py` to pass the `matcher.db` entries to `detect_all`.

## 3. Verification

- [x] 3.1 Verify that `python -m anonymizer.cli detect sample_docs/carta_oferta_4.docx` now finds 'GDP' and 'BRT'.
- [x] 3.2 Verify that the generated Excel mapping for `carta_oferta_4.docx` contains 'GDP' and 'BRT' as expected.
