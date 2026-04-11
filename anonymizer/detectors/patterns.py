import re
from anonymizer.models import Entity, EntityType

# New consolidated pattern list (Single List model)

# New consolidated pattern list (Single List model)
DEFAULT_PATTERNS = [
    {"id": "builtin_dni", "name": "DNI/NIE", "type": EntityType.ID_NUMBER.value, "pattern": r"\b[0-9]{8}[A-Z]\b|\b[XYZ][0-9]{7}[A-Z]\b", "enabled": True, "builtin": True},
    {"id": "builtin_cuit", "name": "CUIT/CUIL", "type": EntityType.ID_NUMBER.value, "pattern": r"\b\d{2}-\d{8}-\d\b", "enabled": True, "builtin": True},
    {"id": "builtin_email", "name": "EMAIL", "type": EntityType.EMAIL.value, "pattern": r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b", "enabled": True, "builtin": True},
    {"id": "builtin_phone_ar", "name": "PHONE_AR", "type": EntityType.PHONE.value, "pattern": r"\b(?:15[-\s]?\d{4}[-\s]?\d{4}|\d{4}[-\s]\d{4}|\d{2}-\d{4}-\d{4}|11[-\s]\d{4}[-\s]?\d{4})\b", "enabled": True, "builtin": True},
    {"id": "builtin_phone_es", "name": "PHONE_ES", "type": EntityType.PHONE.value, "pattern": r"\b(?:\+34\s?)?[6789]\d{2}[\s.\-]?\d{3}[\s.\-]?\d{3}\b", "enabled": True, "builtin": True},
    {"id": "builtin_iban", "name": "IBAN", "type": EntityType.BANK.value, "pattern": r"\b[A-Z]{2}\d{2}[\s]?(?:\d{4}[\s]?){4,6}\d{0,4}\b", "enabled": True, "builtin": True},
    {"id": "builtin_cbu", "name": "CBU_AR", "type": EntityType.BANK.value, "pattern": r"\b\d{22}\b", "enabled": True, "builtin": True},
    {"id": "builtin_phone_int", "name": "PHONE_INT", "type": EntityType.PHONE.value, "pattern": r"\b\+[1-9]\d{1,3}[\s.\-]?\(?\d{1,4}\)?[\s.\-]?\d{1,4}[\s.\-]?\d{1,9}\b", "enabled": True, "builtin": True},
    {"id": "builtin_money", "name": "MONEY", "type": EntityType.MONEY.value, "pattern": r"(?i)(?:\$|USD|ARS|EUR|€|£|¥)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?|\b\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s?(?:Pesos|Dólares|USD|ARS|EUR|ARS|€|£|¥)", "enabled": True, "builtin": True},
    
    # Templates (disabled by default)
    {"id": "tmpl_expediente", "name": "Nro. Expediente", "type": EntityType.CUSTOM.value, "pattern": r"EXP-\d{4}/\d{4}", "enabled": False, "builtin": False},
    {"id": "tmpl_contrato", "name": "Nro. Contrato", "type": EntityType.CUSTOM.value, "pattern": r"CONT-\d+", "enabled": False, "builtin": False},
    {"id": "tmpl_cuenta", "name": "Nro. Cuenta Bancaria", "type": EntityType.BANK.value, "pattern": r"\d{3}-\d{6}-\d{2}", "enabled": False, "builtin": False},
    {"id": "tmpl_patente", "name": "Patente Vehicular", "type": EntityType.CUSTOM.value, "pattern": r"[A-Z]{2}\d{3}[A-Z]{2}|[A-Z]{3}\d{3}", "enabled": False, "builtin": False},
]


def detect(text: str, patterns: list[dict] | None = None) -> list[Entity]:
    """
    Detect structured entities via regex.
    patterns: list of {"name": str, "type": str, "pattern": str, "enabled": bool}
    """
    if not patterns:
        return []

    entities: list[Entity] = []
    seen: set[tuple[int, int, str]] = set()

    for p in patterns:
        if not p.get("enabled", True):
            continue
            
        name = p.get("name", "UNNAMED")
        etype_str = p.get("type", "PERSONALIZADO")
        pattern_str = p.get("pattern", "")
        
        if not pattern_str:
            continue

        try:
            etype = EntityType(etype_str)
        except ValueError:
            # Handle mapping legacy or inconsistent names
            mapping = {
                "DNI/NIE": EntityType.ID_NUMBER,
                "CUIT/CUIL": EntityType.ID_NUMBER,
                "PERSONALIZADO": EntityType.CUSTOM
            }
            etype = mapping.get(etype_str, EntityType.CUSTOM)

        try:
            for m in re.finditer(pattern_str, text):
                span = (m.start(), m.end(), etype.value)
                if span not in seen:
                    seen.add(span)
                    entities.append(Entity(
                        text=m.group(),
                        entity_type=etype,
                        start=m.start(),
                        end=m.end(),
                        source="regex",
                    ))
        except Exception:
            # Skip invalid regex
            continue

    return entities
