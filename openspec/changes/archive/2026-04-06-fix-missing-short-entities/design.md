## Context

The system has a hardcoded limit in `anonymizer/detectors/ner.py` that discards entities shorter than 4 characters. This causes 3-letter acronyms like 'GDP' or 'BRT' to be missing from the detection grid even if they are in the database. Furthermore, the detection process is purely heuristic (NER + Regex) and does not use the Known Entities database as a source for discovery.

## Goals / Non-Goals

**Goals:**
- Enable detection of 3-letter entities (Acronyms).
- Use the Known Entities database as a proactive detection source.
- Ensure overlapped detections (e.g., NER finding 'Global Development Partners' while DB scanner finds 'GDP') are handled correctly (deduplicated).

**Non-Goals:**
- Fuzzy matching during the detection phase (too slow). Only exact matching for the proactive scan.

## Decisions

**Decision 1: Lower character threshold in NER**
Change the `len(text) < 4` check to `3` in `ner.py`.
*Rationale:* 3 characters is a very common length for organizational acronyms. The existing stops list and type filters should prevent excessive noise.

**Decision 2: Implement `KnownEntityDetector`**
Create a new module or function within `detector.py` that accepts a list of `KnownEntity` objects and performs a regex search for each form (original and aliases) on the full document text, respecting word boundaries.
*Rationale:* This turns the "Database" into a primary search engine, ensuring that anything the user has already classified is never missed.

**Decision 3: Update deduplication logic**
Prioritize "Source: Known" detections over "Source: NER" when locations overlap.
*Rationale:* Explicitly defined entities are more reliable than general model extractions.

## Risks / Trade-offs

- [Risk]: Searching for many common short strings in the whole document might have a performance impact.
  → Mitigation: Use a compiled regex or an efficient substring search algorithm (like Aho-Corasick if needed, although standard regex is likely fine for typical DB sizes).
