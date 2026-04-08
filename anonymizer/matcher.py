"""
Matches detected entities against the known_entities database.
Returns pre-approved mappings (exact) and fuzzy suggestions (for review).
"""
from dataclasses import dataclass
from rapidfuzz import fuzz, process as rfprocess
from anonymizer.known_entities import KnownEntity
from anonymizer.config import current_settings


@dataclass
class MatchResult:
    detected_text: str       # text as found in the document
    known: KnownEntity       # matched known entity
    score: float             # 100.0 = exact, <100 = fuzzy
    is_exact: bool


class EntityMatcher:
    def __init__(self, db_path=None):
        from anonymizer.known_entities import load
        self.db = load(db_path) if db_path else load()

    def match(self, text: str, entity_type=None) -> str | None:
        """
        Retorna el pseudónimo si hay coincidencia exacta (ignora mayúsculas/minúsculas).
        """
        text_lower = text.lower().strip()
        for ke in self.db:
            if any(form.lower() == text_lower for form in ke.all_forms):
                return ke.pseudonym
        return None


def match_against_db(
    detected_texts: list[str],
    known_entities: list[KnownEntity],
    threshold: float = current_settings.fuzzy_threshold,
) -> tuple[list[MatchResult], list[str]]:
    """
    For each detected text:
      - Exact match  → MatchResult(is_exact=True)
      - Fuzzy match  → MatchResult(is_exact=False)
      - No match     → goes into unmatched list

    Returns (matches, unmatched_texts)
    """
    if not known_entities:
        return [], detected_texts

    # Build lookup: all forms → KnownEntity
    form_to_entity: dict[str, KnownEntity] = {}
    for ke in known_entities:
        for form in ke.all_forms:
            form_to_entity[form.lower()] = ke

    all_forms = list(form_to_entity.keys())

    matches: list[MatchResult] = []
    unmatched: list[str] = []

    for text in detected_texts:
        text_lower = text.lower()

        # 1. Exact match (case-insensitive)
        if text_lower in form_to_entity:
            ke = form_to_entity[text_lower]
            matches.append(MatchResult(
                detected_text=text,
                known=ke,
                score=100.0,
                is_exact=True,
            ))
            continue

        # 2. Fuzzy match
        result = rfprocess.extractOne(
            text_lower,
            all_forms,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=threshold,
        )
        if result:
            best_form, score, _ = result
            ke = form_to_entity[best_form]
            matches.append(MatchResult(
                detected_text=text,
                known=ke,
                score=score,
                is_exact=False,
            ))
        else:
            unmatched.append(text)

    return matches, unmatched


def build_mapping_from_matches(matches: list[MatchResult]) -> dict[str, str]:
    """Convert confirmed matches into a replacement mapping."""
    return {m.detected_text: m.known.pseudonym for m in matches}
