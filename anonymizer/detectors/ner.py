from __future__ import annotations
from anonymizer.models import Entity, EntityType
from anonymizer.config import current_settings

# spaCy label → EntityType
_LABEL_MAP = {
    "PER":    EntityType.PERSON,
    "PERSON": EntityType.PERSON,
    "ORG":    EntityType.ORG,
    "LOC":    EntityType.LOCATION,
    "GPE":    EntityType.LOCATION,
}

_nlp = None


def _load_model():
    global _nlp
    if _nlp is not None:
        return _nlp

    import spacy

    for model in current_settings.ner_models:
        try:
            _nlp = spacy.load(model)
            return _nlp
        except OSError:
            continue

    raise RuntimeError(
        "No se encontró ningún modelo de spaCy. Instala uno con:\n"
        "  python -m spacy download xx_ent_wiki_sm\n"
        "  python -m spacy download es_core_news_sm"
    )


def _extract_from_span(ent, char_offset: int) -> Entity | None:
    """Convert a spaCy entity to our Entity, applying filters. Returns None if filtered."""
    etype = _LABEL_MAP.get(ent.label_)
    if etype is None:
        return None
    text = ent.text.strip()
    if len(text) < 3:
        return None
    if text.lower() in current_settings.ner_stopwords:
        return None
    if all(c.isdigit() or c in ".,-%$/\n\t " for c in text):
        return None
    # Sanity: entities should never cross lines (guards against residual merges)
    if "\n" in text:
        return None
    return Entity(
        text=text,
        entity_type=etype,
        start=ent.start_char + char_offset,
        end=ent.end_char + char_offset,
        source="ner",
    )


def detect(text: str) -> list[Entity]:
    """
    Run NER on text, processing each line independently.

    Processing line-by-line prevents spaCy from merging entities that appear
    on consecutive lines (e.g. "Ricardo Gómez\\nEmpresa Asociada" being
    tagged as a single entity span).
    """
    nlp = _load_model()
    entities = []
    char_offset = 0

    for line in text.split("\n"):
        if line.strip():
            line_doc = nlp(line)
            for ent in line_doc.ents:
                entity = _extract_from_span(ent, char_offset)
                if entity is not None:
                    entities.append(entity)
        # Advance offset: length of line + the \n separator
        char_offset += len(line) + 1

    return entities
