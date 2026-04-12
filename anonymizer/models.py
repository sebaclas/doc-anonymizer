from dataclasses import dataclass, field
from enum import Enum


class EntityType(str, Enum):
    PERSON = "PERSONA"
    ORG = "ORGANIZACIÓN"
    LOCATION = "LUGAR"
    DATE = "FECHA"
    EMAIL = "EMAIL"
    PHONE = "TELÉFONO"
    ID_NUMBER = "DNI/NIE"
    BANK = "CUENTA BANCARIA"
    MONEY = "MONTO"
    CUSTOM = "PERSONALIZADO"


@dataclass
class Entity:
    text: str
    entity_type: EntityType
    start: int
    end: int
    source: str  # "ner" | "regex" | "manual"
    context: str = ""

    def __hash__(self):
        return hash((self.text, self.entity_type))

    def __eq__(self, other):
        return self.text == other.text and self.entity_type == other.entity_type


@dataclass
class Document:
    path: str
    paragraphs: list[str] = field(default_factory=list)
    full_text: str = ""
