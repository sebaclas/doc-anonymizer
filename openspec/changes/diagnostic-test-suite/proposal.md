# Proposal: Diagnostic Test Suite

## Why
Currently, identifying why certain entities are not being detected is a manual and repetitive process. Users find words or regex patterns that should be caught but aren't, often due to complex interactions between NER filters (stop-words, length), regex word boundaries, or detection priority shadowing.

A structured diagnostic suite will:
1. Provide a reliable way to capture and reproduce "missed" detections.
2. Automate the "autopsy" of a failure (is it a stop-word? shadowed? regex mismatch?).
3. Ensure that once fixed, these cases never regress.

## What
A regression-based testing system consisting of:
- **Case Inventory**: A structured file (`regression_cases.json`) to store problematic snippets and expected entities.
- **Diagnostic Engine**: A script (`diagnose.py`) that runs the full detection pipeline and reports why a specific entity was or wasn't found.
- **CLI Integration**: Ability to run these tests easily from the terminal.

## How
1. Create a `tests/` directory structure for regression cases.
2. Implement a diagnostic script that inspects the internal state of `detect_all` (source of detection, filters applied).
3. Integrate with the existing `anonymizer` logic without modifying core production code.

## Risks
- **Maintenance**: Keeping the test cases updated as the document structure changes.
- **False Positives**: Ensuring the diagnostic tool itself correctly identifies the cause of failure.
