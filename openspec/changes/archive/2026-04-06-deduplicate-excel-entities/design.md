## Context

The current document anonymization workflow detects entities (NER + rules) and generates a list of entities. These entities are mapped to their pseudonyms via `EntityMatcher` and then all exported to an Excel file so the user can review/edit the mapping. However, multiple identical occurrences of the same entity (e.g., "Juan Perez" appearing 5 times) yield 5 identical rows in the generated Excel output, forcing users to repeatedly manually fill in or review the same mapped values.

## Goals / Non-Goals

**Goals:**
- Eliminate duplicate rows in the generated Excel files for both CLI and GUI usage.
- Deduplication should be based on a unique combination of `text` and `entity_type`.
- The document anonymization itself should continue replacing all instances correctly (which is naturally supported by passing a `{text: pseudonym}` dictionary).

**Non-Goals:**
- Do not change how the entity detection algorithm finds positions inside the document.

## Decisions

**Decision 1: Where to deduplicate?**
We will implement the deduplication right before building the "rows" list that will be dumped into Excel in both `cli.py` and `gui.py`. 
*Rationale:* Deduplicating inside the core `detector.detect_all` might strip positional data for multiple occurrences of an entity that might be useful later (e.g., for analytics, highlighting in a viewer). Deduplicating only at the Excel export step ensures the review interface is clean without loss of potentially useful information from the detection phase.
*Alternative considered:* Modifying `detector._deduplicate` to group by text. Rejected because it drops positional information of subsequent occurrences which could be needed later.

**How:** 
Use a `seen` set containing tuples of `(ent.text, ent.entity_type)` to track what has already been processed during the loop that builds the `rows` list.

## Risks / Trade-offs

- [Risk] If an entity has multiple types detected (e.g. "Washington" as PERSON and "Washington" as LOCATION), it will appear twice in the Excel. 
  → Mitigation: This is desirable, as the user might want to map different pseudonyms based on the entity type context.
