import re
from anonymizer.models import Entity, EntityType

# (name, type, pattern)
BUILTIN_PATTERNS: list[tuple[str, EntityType, str]] = [
    ("DNI/NIE",    EntityType.ID_NUMBER, r"\b[0-9]{8}[A-Z]\b|\b[XYZ][0-9]{7}[A-Z]\b"),
    ("CUIT/CUIL",  EntityType.ID_NUMBER, r"\b\d{2}-\d{8}-\d\b"),
    ("EMAIL",      EntityType.EMAIL,     r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"),
    ("PHONE_AR",   EntityType.PHONE,     r"\b(?:15[-\s]?\d{4}[-\s]?\d{4}|\d{4}[-\s]\d{4}|\d{2}-\d{4}-\d{4}|11[-\s]\d{4}[-\s]?\d{4})\b"),
    ("PHONE_ES",   EntityType.PHONE,     r"\b(?:\+34\s?)?[6789]\d{2}[\s.\-]?\d{3}[\s.\-]?\d{3}\b"),
    ("IBAN",       EntityType.BANK,      r"\b[A-Z]{2}\d{2}[\s]?(?:\d{4}[\s]?){4,6}\d{0,4}\b"),
    ("CBU_AR",     EntityType.BANK,      r"\b\d{22}\b"),
    ("PHONE_INT",  EntityType.PHONE,     r"\b\+[1-9]\d{1,3}[\s.\-]?\(?\d{1,4}\)?[\s.\-]?\d{1,4}[\s.\-]?\d{1,9}\b"),
    ("MONEY",      EntityType.MONEY,     r"(?i)(?:\$|USD|ARS|EUR|€|£|¥)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?|\b\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s?(?:Pesos|Dólares|USD|ARS|EUR|ARS|€|£|¥)"),
]


def detect(text: str, custom_patterns: list[dict] | None = None) -> list[Entity]:
    """
    Detect structured entities via regex.
    custom_patterns: list of {"name": str, "type": str, "pattern": str}
    """
    patterns = list(BUILTIN_PATTERNS)

    if custom_patterns:
        for cp in custom_patterns:
            try:
                etype = EntityType(cp["type"])
            except ValueError:
                etype = EntityType.CUSTOM
            patterns.append((cp["name"], etype, cp["pattern"]))

    entities: list[Entity] = []
    seen: set[tuple[int, int]] = set()

    for _name, etype, pattern in patterns:
        for m in re.finditer(pattern, text):
            span = (m.start(), m.end())
            if span not in seen:
                seen.add(span)
                entities.append(Entity(
                    text=m.group(),
                    entity_type=etype,
                    start=m.start(),
                    end=m.end(),
                    source="regex",
                ))

    return entities
