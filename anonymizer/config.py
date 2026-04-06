"""
Loads custom patterns from a JSON config file.

Format of custom_patterns.json:
[
  {
    "name": "Número de expediente",
    "type": "PERSONALIZADO",
    "pattern": "EXP-\\d{4,8}"
  }
]
"""
import json
from pathlib import Path

DEFAULT_CONFIG_PATH = Path.home() / ".doc-anonymizer" / "custom_patterns.json"


def load_custom_patterns(path: str | Path | None = None) -> list[dict]:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return []
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"El archivo de config debe ser una lista JSON: {config_path}")
    return data


def create_default_config(path: str | Path | None = None):
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
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
