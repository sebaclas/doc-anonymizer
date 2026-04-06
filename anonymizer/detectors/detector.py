from anonymizer.models import Entity, Document
from anonymizer.detectors import ner, patterns as pat_module


def detect_all(
    doc: Document,
    custom_patterns: list[dict] | None = None,
    use_ner: bool = True,
) -> list[Entity]:
    """
    Run NER + regex on the document's full text.
    use_ner=False skips NER entirely (useful for contracts/legal docs).
    """
    ner_entities = ner.detect(doc.full_text) if use_ner else []
    regex_entities = pat_module.detect(doc.full_text, custom_patterns)

    all_entities = ner_entities + regex_entities
    return _deduplicate(all_entities)


def _deduplicate(entities: list[Entity]) -> list[Entity]:
    # Sort by start position
    sorted_ents = sorted(entities, key=lambda e: (e.start, -(e.end - e.start)))

    result: list[Entity] = []
    last_end = -1

    for ent in sorted_ents:
        if ent.start >= last_end:
            result.append(ent)
            last_end = ent.end
        # If overlapping, keep the first (longer/earlier) one

    return result
