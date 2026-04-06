# Design: Monetary Amount Detection

## Overview
This change adds a new entity category for monetary values, enhancing detection beyond standard NER capabilities. It implements a regex-based approach within the existing pattern detection pipeline.

## Architectural Changes

### 1. Model Extension
- **File**: `anonymizer/models.py`
- **Change**: Add `MONEY = "MONTO"` to `EntityType`.

### 2. Pattern Detection
- **File**: `anonymizer/detectors/patterns.py`
- **Change**: Add new patterns to `BUILTIN_PATTERNS`.
- **Regex Logic**: 
    - `MONEY_PREFIX`: Matches symbols (+ optional space) + numbers.
    - `MONEY_SUFFIX`: Matches numbers (+ optional space) + currency names/shortcodes.
    - Pattern example: `(?i)(?:\$|USD|ARS|EUR|€)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?`
    - Pattern example: `\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s?(?:Pesos|Dólares|USD|ARS|EUR|€)`

## Data Flow
1. `detector.detect_all` is called.
2. `pat_module.detect` runs the new `MONEY` regex along with others.
3. Entities are returned as `Entity(entity_type=EntityType.MONEY, source="regex")`.
4. In the Excel workflow, these will be suggested with `accion="s"` (default for regex).
