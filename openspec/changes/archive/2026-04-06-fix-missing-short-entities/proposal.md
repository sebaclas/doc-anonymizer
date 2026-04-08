## Why

Currently, the system fails to detect important 3-letter entities such as 'GDP' and 'BRT' even if they are defined in the Known Entities database. This is caused by an aggressive length filter in the NER extraction module that discards any entity shorter than 4 characters. Additionally, the system relies purely on NER/Regex for detection, meaning terms in the database are not proactively found unless previously detected by those engines.

## What Changes

- Lower the minimum character threshold for NER entities from 4 to 3 to include common organizational acronyms.
- Implement a **Proactive Database Detection** step: the system will scan the document for all exact matches of entries in the Known Entities database, ensuring these are always caught regardless of NER performance.
- Update the deduplication logic to prioritize DB-matched entities over NER or Regex extractions in case of overlaps.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `entity-detection`: Requirements changed to include proactive matching against the Known Entities DB alongside NER and Patterns.

## Impact

- `anonymizer/detectors/ner.py`: Reduce length filter.
- `anonymizer/detectors/detector.py`: Add a new step to find known entities.
- `anonymizer/cli.py` and `anonymizer/gui.py`: Pass the loaded DB entities to the detector.
