import re
from anonymizer.models import Entity, Document, EntityType
from anonymizer.detectors import ner, patterns as pat_module


def detect_all(
    doc: Document,
    patterns: list[dict] | None = None,
    use_ner: bool = True,
    known_entities: list = None,
) -> list[Entity]:
    """
    Run NER + regex + known lookup on the document's full text.
    use_ner=False skips NER entirely.
    """
    from anonymizer.config import load_custom_patterns
    from anonymizer.known_entities import load
    
    # If no patterns provided, load from config
    active_patterns = patterns if patterns is not None else load_custom_patterns()
    
    # If no known_entities provided, load from master Excel
    shared_known = known_entities if known_entities is not None else load()
    
    known_entities_found = _detect_known(doc.full_text, shared_known) if shared_known else []
    ner_entities = ner.detect(doc.full_text) if use_ner else []
    regex_entities = pat_module.detect(doc.full_text, active_patterns)

    all_entities = known_entities_found + ner_entities + regex_entities
    return _deduplicate(all_entities)


def _get_etype(etype_str: str) -> EntityType:
    try:
        return EntityType(etype_str)
    except ValueError:
        # Fallback for mapping common strings to enum values
        mapping = {
            "ORGANIZACION": EntityType.ORG,
            "ORGANIZACIÓN": EntityType.ORG,
            "PERSONA": EntityType.PERSON,
            "LUGAR": EntityType.LOCATION,
            "FECHA": EntityType.DATE,
            "EMAIL": EntityType.EMAIL,
            "TELÉFONO": EntityType.PHONE,
            "DNI": EntityType.ID_NUMBER,
            "PERSONALIZADO": EntityType.CUSTOM,
        }
        return mapping.get(etype_str.upper(), EntityType.CUSTOM)


def _detect_known(text: str, known_entities: list) -> list[Entity]:
    """Proactively find exact matches of known entities in the text."""
    entities: list[Entity] = []
    if not known_entities:
        return entities

    for ke in known_entities:
        for form in ke.all_forms:
            if not form.strip():
                continue
            
            pattern = re.escape(form)
            # Use word boundaries if requested (default)
            if getattr(ke, "match_mode", "palabra") == "palabra":
                pattern = rf"\b{pattern}\b"
            
            etype = _get_etype(getattr(ke, "entity_type", "PERSONALIZADO"))
            
            for m in re.finditer(pattern, text, re.IGNORECASE):
                entities.append(Entity(
                    text=m.group(),
                    entity_type=etype,
                    start=m.start(),
                    end=m.end(),
                    source="known",
                ))
    return entities


def _deduplicate(entities: list[Entity]) -> list[Entity]:
    # Sort by start position, then by source priority (known > regex > ner), then length
    priority = {"known": 0, "regex": 1, "ner": 2}
    sorted_ents = sorted(entities, key=lambda e: (
        e.start, 
        priority.get(e.source, 3), 
        -(e.end - e.start)
    ))

    result: list[Entity] = []
    last_end = -1

    for ent in sorted_ents:
        if ent.start >= last_end:
            result.append(ent)
            last_end = ent.end
        # If overlapping, keep the first (earlier/higher priority) one

    return result
