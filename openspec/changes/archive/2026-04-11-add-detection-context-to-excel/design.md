## Context

The current entity detection workflow produces a list of unique terms in Excel, but without the surrounding text, it's often impossible for the user to determine if "Empresa Estatal" refers to the company or is part of a longer unrelated string, or if a generic name is indeed the person they are looking for.

## Goals / Non-Goals

**Goals:**
- Provide a 5-word lookahead/lookbehind window for every detection.
- Display this context in the Excel vetting file with the match highlighted.
- Support both GUI and CLI workflows.

**Non-Goals:**
- Storing multiple contexts for the same entity in the mapping file (only the first occurrence is shown for brevity).
- Implementing context in the Master Database (it is only for the interactive mapping Excel).

## Decisions

- **Data Model**: Add `context: str` to the `Entity` dataclass in `anonymizer/models.py`.
- **Extraction Logic**: Implement a helper `_extract_context(text, start, end, window=5)` in `anonymizer/detectors/detector.py`.
    - Rationale: Using word-based splitting (`text.split()`) ensures we don't show half-words.
    - Match highlighting: The match will be wrapped in `[]` within the context string.
- **Excel Layout**: Add the "Contexto" column as the second column in the "Detecciones" sheet.
    - Rationale: Placing it right next to "Original" makes it easier for the eye to scan during vetting.
- **Deduplication**: In the GUI and CLI layers, when converting detections to Excel rows, use the `context` from the first `Entity` instance encountered for each unique `(text, type)` pair.

## Risks / Trade-offs

- **Memory overhead**: Every `Entity` object will now hold a string of ~10-12 words. For documents with thousands of detections, this might increase memory usage significantly.
    - *Mitigation*: The context strings are small (avg 100-200 chars). Even with 10k detections, it's only ~2MB additional RAM.
- **Performance**: Splitting text repeatedly.
    - *Mitigation*: Only split the local slice of text `text[max(0, start-100):min(len(text), end+100)]` instead of the whole document.
