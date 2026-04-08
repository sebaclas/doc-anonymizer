"""
Settings management for the document anonymizer.
"""
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)

APP_DIR = Path.home() / ".doc-anonymizer"
SETTINGS_PATH = APP_DIR / "settings.json"

# Default constants (previously hardcoded in other modules)
DEFAULT_NER_MODELS = [
    "xx_ent_wiki_sm",   # multilingual (recommended)
    "es_core_news_sm",  # Spanish
    "en_core_web_sm",   # English fallback
]

DEFAULT_STOPWORDS = {
    # Financial
    "total", "subtotal", "saldo", "cuil", "cuit", "nombre", "gasto", "gastos",
    "ingresos", "egresos", "intereses", "generales", "pagos", "período", "periodo",
    "monto", "importe", "precio", "valor", "cuota", "factura", "recibo", "pago",
    # Legal / contract terms
    "contrato", "contratante", "contratista", "proveedor", "cliente", "parte",
    "partes", "empresa", "sociedad", "entidad", "organismo", "estado", "nacion",
    "servicio", "servicios", "producto", "productos", "objeto", "cláusula",
    "clausula", "anexo", "acuerdo", "convenio", "rescisión", "rescision",
    "incumplimiento", "penalidad", "garantía", "garantia", "plazo", "vigencia",
    "jurisdicción", "jurisdiccion", "tribunal", "juzgado", "fuero", "ley",
    "decreto", "resolución", "resolucion", "artículo", "articulo", "inciso",
    "obligación", "obligacion", "derecho", "derechos", "responsabilidad",
    "confidencialidad", "propiedad", "intelectual", "licencia", "cesión",
    "cesion", "representante", "apoderado", "domicilio", "notificación",
    "notificacion", "firmante", "suscribiente", "abajo", "presente",
    # Generic capitalized words
    "no", "si", "lugar", "edificio", "seg", "ascensores", "portero",
    "lula", "tanq", "limp", "cta", "juri", "yami", "bolsas",
    "administración", "administracion", "señor", "señora", "señores",
    "considerando", "resultando", "visto", "acuerdo", "mediante",
}

DEFAULT_FUZZY_THRESHOLD = 85


@dataclass
class Settings:
    db_path: str = str(APP_DIR / "known_entities.json")
    patterns_path: str = str(APP_DIR / "custom_patterns.json")
    ner_models: list[str] = field(default_factory=lambda: list(DEFAULT_NER_MODELS))
    ner_stopwords: list[str] = field(default_factory=lambda: sorted(list(DEFAULT_STOPWORDS)))
    fuzzy_threshold: int = DEFAULT_FUZZY_THRESHOLD

    def save(self, path: Path | None = None):
        """Save settings to JSON."""
        save_path = path or SETTINGS_PATH
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: Path | None = None) -> "Settings":
        """Load settings from JSON, merging with defaults."""
        load_path = path or SETTINGS_PATH
        if not load_path.exists():
            settings = cls()
            settings.save(load_path)
            # Ensure the default patterns file is also created for a fresh install
            create_default_config()
            return settings

        try:
            with open(load_path, encoding="utf-8") as f:
                data = json.load(f)
            
            # Merit merge: only overwrite fields present in JSON
            # This ensures that if new settings are added to the class in the future,
            # old settings.json files won't break the app.
            default_data = asdict(cls())
            for key in default_data:
                if key not in data:
                    data[key] = default_data[key]
            
            return cls(**data)
        except Exception as e:
            logger.warning(f"Error cargando configuración ({load_path}): {e}. Usando defaults.")
            return cls()


# Global singleton
current_settings = Settings.load()


def load_custom_patterns(path: str | Path | None = None) -> list[dict]:
    """Legacy helper maintained for compatibility, now points to settings.patterns_path."""
    config_path = Path(path) if path else Path(current_settings.patterns_path)
    if not config_path.exists():
        return []
    try:
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except Exception:
        return []


def create_default_config(path: str | Path | None = None):
    """Legacy helper maintained for compatibility."""
    config_path = Path(path) if path else Path(current_settings.patterns_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    example = [
        {
            "name": "Número de expediente",
            "type": "PERSONALIZADO",
            "pattern": "EXP-\\d{4,8}"
        }
    ]
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(example, f, ensure_ascii=False, indent=2)
    return config_path
