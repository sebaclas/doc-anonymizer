"""
Persistent database of known entities and their fixed pseudonyms.
Stored at ~/.doc-anonymizer/known_entities.json
"""
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from anonymizer.models import EntityType

DB_PATH = Path.home() / ".doc-anonymizer" / "known_entities.json"


@dataclass
class KnownEntity:
    original: str
    pseudonym: str
    entity_type: str  # EntityType.value string
    aliases: list[str]  # alternative spellings / abbreviations
    match_mode: str = "palabra"  # "palabra" = word boundaries (\b), "substring" = anywhere

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "KnownEntity":
        return KnownEntity(
            original=d["original"],
            pseudonym=d["pseudonym"],
            entity_type=d.get("entity_type", EntityType.CUSTOM.value),
            aliases=d.get("aliases", []),
            match_mode=d.get("match_mode", "palabra"),
        )

    @property
    def all_forms(self) -> list[str]:
        """All text forms that should match this entity."""
        return [self.original] + self.aliases


def load(path: Path | None = None) -> list[KnownEntity]:
    db_path = path or DB_PATH
    if not db_path.exists():
        # Aseguramos que el directorio exista para futuras escrituras
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return []
    try:
        with open(db_path, encoding="utf-8") as f:
            data = json.load(f)
        return [KnownEntity.from_dict(e) for e in data]
    except (json.JSONDecodeError, ValueError):
        # Si el archivo está corrupto o vacío, devolvemos lista vacía
        return []


def save(entities: list[KnownEntity], path: Path | None = None):
    db_path = path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in entities], f, ensure_ascii=False, indent=2)


def add(entity: KnownEntity, path: Path | None = None):
    entities = load(path)
    # Replace if original already exists
    entities = [e for e in entities if e.original != entity.original]
    entities.append(entity)
    save(entities, path)


def remove(original: str, path: Path | None = None) -> bool:
    entities = load(path)
    before = len(entities)
    entities = [e for e in entities if e.original != original]
    if len(entities) < before:
        save(entities, path)
        return True
    return False


def import_from_mapping(mapping: dict[str, str], entity_type: str = "PERSONALIZADO",
                         path: Path | None = None):
    """Bulk-import from an existing JSON mapping dict."""
    entities = load(path)
    existing = {e.original for e in entities}
    added = 0
    for original, pseudonym in mapping.items():
        if original not in existing and pseudonym:
            entities.append(KnownEntity(
                original=original,
                pseudonym=pseudonym,
                entity_type=entity_type,
                aliases=[],
            ))
            added += 1
    save(entities, path)
    return added


def to_excel(excel_path: Path, db_path: Path | None = None):
    """Export the DB to an editable Excel file."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment

    entities = load(db_path)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Entidades conocidas"

    headers = ["Original", "Pseudonimo", "Tipo", "Aliases (separados por coma)", "Modo"]
    header_fill = PatternFill("solid", fgColor="2E75B6")
    header_font = Font(bold=True, color="FFFFFF")

    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    for row_idx, e in enumerate(entities, start=2):
        ws.cell(row=row_idx, column=1, value=e.original)
        ws.cell(row=row_idx, column=2, value=e.pseudonym)
        ws.cell(row=row_idx, column=3, value=e.entity_type)
        ws.cell(row=row_idx, column=4, value=", ".join(e.aliases) if e.aliases else "")
        ws.cell(row=row_idx, column=5, value=e.match_mode)

    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 35
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 40
    ws.column_dimensions["E"].width = 12

    # Freeze header row
    ws.freeze_panes = "A2"

    wb.save(str(excel_path))
    return len(entities)


def from_excel(excel_path: Path, db_path: Path | None = None) -> tuple[int, int]:
    """
    Import/update the DB from an Excel file.
    Rows with empty Original or Pseudonimo are skipped.
    Returns (updated_count, added_count).
    """
    import openpyxl

    wb = openpyxl.load_workbook(str(excel_path))
    ws = wb.active

    existing = {e.original: e for e in load(db_path)}
    updated = added = 0

    for row in ws.iter_rows(min_row=2, values_only=True):
        original = str(row[0]).strip() if row[0] else ""
        pseudonym = str(row[1]).strip() if row[1] else ""
        entity_type = str(row[2]).strip() if row[2] else "PERSONALIZADO"
        aliases_raw = str(row[3]).strip() if row[3] else ""
        aliases = [a.strip() for a in aliases_raw.split(",") if a.strip()] if aliases_raw else []
        match_mode_raw = str(row[4]).strip().lower() if len(row) > 4 and row[4] else "palabra"
        match_mode = match_mode_raw if match_mode_raw in ("palabra", "substring") else "palabra"

        if not original or not pseudonym:
            continue

        if original in existing:
            e = existing[original]
            e.pseudonym = pseudonym
            e.entity_type = entity_type
            e.aliases = aliases
            e.match_mode = match_mode
            updated += 1
        else:
            existing[original] = KnownEntity(
                original=original,
                pseudonym=pseudonym,
                entity_type=entity_type,
                aliases=aliases,
                match_mode=match_mode,
            )
            added += 1

    save(list(existing.values()), db_path)
    return updated, added
