# Tasks: Diagnostic Test Suite

## Setup
- [ ] Create directory `tests/regression/`
- [ ] Initialize `tests/regression/cases.csv` with an empty list `[]`

## Implementation
- [ ] Develop `anonymizer/diagnostics.py`
    - [ ] Import `_STOPWORDS` and `_LABEL_MAP` from `anonymizer.detectors.ner`
    - [ ] Import `BUILTIN_PATTERNS` from `anonymizer.detectors.patterns`
    - [ ] Implement `check_filters(text)` logic
    - [ ] Implement `check_shadowing(all_entities, target_span)` logic
- [ ] Create `scripts/run_diagnostics.py`
    - [ ] CLI argument parsing (file path, verbosity)
    - [ ] Result table formatting (using `tabulate` if available or simple print)
    - [ ] Logic to load and iterate over `cases.csv`

## Verification
- [ ] Add 2 known "failing" cases (e.g., a word in Stopwords and an overlapping span)
- [ ] Run diagnostic script and verify it correctly identifies the cause of failure
- [ ] Add 1 "passing" case and verify it reports success

## Documentation
- [ ] Update `MANUAL.md` with instructions on how to use the diagnostic suite to report bugs
