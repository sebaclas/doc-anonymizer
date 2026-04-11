# Design: Diagnostic Test Suite

## Architecture
The diagnostic suite iterates over a collection of test cases and performs a multi-level inspection of the detection pipeline.

### Data Model
`tests/regression/cases.csv` format:
```csv
id,text,expected,type
case_001,La AFIP emitió una resolución...,AFIP,ORG
```

### Components

#### 1. Diagnostic Hub (`anonymizer/diagnostics.py`)
This module will provide the core diagnostic logic:
- `analyze_span(text, target_text)`:
    - **Step 1: Raw Regex Check**: Search for `target_text` using a simple `re.search`.
    - **Step 2: Filter Check**: 
        - Is it in `_STOPWORDS`?
        - Is it < 3 chars?
        - Does it contain newlines?
    - **Step 3: Pipeline Execution**: Run `detect_all` and check if `target_text` is in the result.
    - **Step 4: Shadow Detection**: If found in Step 1/2 but missing in Step 3, identify which other entity shadowed it in `_deduplicate`.

#### 2. Test Runner (`scripts/run_diagnostics.py`)
A CLI utility to:
- Load `cases.csv`.
- Run `analyze_span` for each case.
- Output a color-coded table (found, filtered, shadowed, missed).

### User Interface
The user can add cases via the CSV file or a simplified CLI command:
`python scripts/run_diagnostics.py --add "Text here" --expect "Word"`

## Technical Decisions
- **No changes to production logic**: The diagnostic tool will import and use existing detector functions. To inspect private internal filters (like `_STOPWORDS`), we will expose them or import them directly in the diagnostic module.
- **Mocking**: No heavy mocking needed since detectors are mostly pure functions of text.

## Integration
- Integrate with `pytest`.
