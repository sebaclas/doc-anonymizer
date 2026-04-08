from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

app = typer.Typer(
    name="anonymize",
    help="Anonimiza documentos Word (.docx) y PDF pseudonimizando entidades detectadas.",
    add_completion=False,
)

# Sub-app for "db" commands
db_app = typer.Typer(help="Gestiona la base de datos de entidades conocidas.")
app.add_typer(db_app, name="db")

console = Console()


def _get_extractor(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".docx":
        from anonymizer.extractors import docx_extractor
        return docx_extractor.extract
    elif suffix == ".pdf":
        from anonymizer.extractors import pdf_extractor
        return pdf_extractor.extract
    else:
        console.print(f"[red]Formato no soportado: {suffix}. Usa .docx o .pdf[/red]")
        raise typer.Exit(1)


def _output_path(input_path: Path, output: Optional[Path]) -> Path:
    if output:
        return output
    return input_path.parent / f"{input_path.stem}_anonimizado{input_path.suffix}"


# ── MAIN COMMANDS ─────────────────────────────────────────────────────────────

@app.command()
def run(
    document: Path = typer.Argument(..., help="Ruta al documento .docx o .pdf"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    mapping_file: Optional[Path] = typer.Option(None, "--mapping", "-m", help="Mapeo JSON existente"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Patrones custom JSON"),
    excel: bool = typer.Option(True, "--excel/--no-excel"),
    skip_review: bool = typer.Option(False, "--skip-review"),
    fuzzy_threshold: float = typer.Option(85.0, "--threshold", "-t",
                                           help="Umbral de similitud para matching aproximado (0-100)"),
    no_ner: bool = typer.Option(False, "--no-ner",
                                 help="Saltear NER, usar solo regex + base de datos (recomendado para contratos)"),
):
    """Flujo completo: detectar -> match DB -> revisar -> pseudonimizar -> generar documento."""
    from anonymizer import config as cfg_module, mapping as map_module, review as rev_module
    from anonymizer.detectors import detector
    from anonymizer import replacer, known_entities as ke_module, matcher as mat_module

    if not document.exists():
        console.print(f"[red]Archivo no encontrado: {document}[/red]")
        raise typer.Exit(1)

    # 1. Extract
    console.print(f"\n[bold]Procesando:[/bold] {document.name}")
    extract = _get_extractor(document)
    with console.status("Extrayendo texto..."):
        doc = extract(document)
    console.print(f"  [green]OK[/green] {len(doc.paragraphs)} parrafos extraidos")

    # 2. Detect & Match
    known = ke_module.load()
    custom_patterns = cfg_module.load_custom_patterns(config)
    with console.status("Detectando entidades..."):
        entities = detector.detect_all(doc, custom_patterns, use_ner=not no_ner, known_entities=known)
    console.print(f"  [green]OK[/green] {len(entities)} entidades detectadas")

    # 3. Match against known entities DB
    detected_texts = list({e.text for e in entities})
    db_matches, unmatched_texts = mat_module.match_against_db(
        detected_texts, known, threshold=fuzzy_threshold
    )

    final_mapping: dict[str, str] = {}

    if not skip_review:
        # 3a. Review known matches (auto-approve exact, confirm fuzzy)
        if db_matches:
            approved_from_db, _ = rev_module.review_known_matches(db_matches)
            final_mapping.update(approved_from_db)

        # 3b. Review unknown entities interactively
        unknown_entities = [e for e in entities if e.text in unmatched_texts]
        confirmed_new = rev_module.review_entities(unknown_entities)
    else:
        # Skip review: auto-approve all DB matches, include all detected
        final_mapping.update(mat_module.build_mapping_from_matches(db_matches))
        confirmed_new = [e for e in entities if e.text in unmatched_texts]

    # 4. Load existing mapping if provided
    if mapping_file:
        final_mapping.update(map_module.load_json(mapping_file))

    # 5. Fill pseudonyms for new entities
    new_mapping = map_module.build_mapping(confirmed_new, final_mapping)
    empty_keys = map_module.validate(new_mapping)
    if empty_keys:
        console.print(f"\n[bold cyan]Asigna pseudonimos para {len(empty_keys)} entidades nuevas:[/bold cyan]\n")
        for key in empty_keys:
            # Re-ask until user provides a non-empty pseudonym
            while True:
                pseudo = Prompt.ask(f"  [white]{key}[/white] -> pseudonimo")
                if pseudo.strip():
                    break
                console.print("  [yellow]El pseudonimo no puede estar vacio.[/yellow]")

            new_mapping[key] = pseudo

            # Offer to save to DB
            save_choice = Prompt.ask(
                f"  [dim]Guardar \"{key}\" -> \"{pseudo}\" en la base de datos?[/dim] [green]S[/green]i / [red]N[/red]o",
                choices=["s", "n", "S", "N"],
                default="s",
            ).lower()
            if save_choice == "s":
                from anonymizer.models import EntityType
                etype = next(
                    (e.entity_type.value for e in confirmed_new if e.text == key),
                    EntityType.CUSTOM.value,
                )
                ke_module.add(ke_module.KnownEntity(
                    original=key,
                    pseudonym=pseudo,
                    entity_type=etype,
                    aliases=[],
                ))
                console.print(f"  [green]OK[/green] Guardado en base de datos")

    final_mapping.update(new_mapping)

    if not final_mapping:
        console.print("[yellow]Sin entidades confirmadas. Operacion cancelada.[/yellow]")
        raise typer.Exit(0)

    # 6. Build modes dict from the known-entities DB (for word-boundary control)
    # Re-load DB after any saves done during pseudonym assignment
    known_reloaded = ke_module.load()
    modes: dict[str, str] = {}
    # Index by original and aliases
    known_index: dict[str, ke_module.KnownEntity] = {}
    for ke in known_reloaded:
        known_index[ke.original] = ke
        for alias in ke.aliases:
            known_index[alias] = ke
    for key in final_mapping:
        if key in known_index:
            modes[key] = known_index[key].match_mode
        else:
            modes[key] = "palabra"  # safe default for new entities

    # 7. Save mapping files
    out_path = _output_path(document, output)
    mapping_json_path = out_path.parent / f"{out_path.stem}_mapeo.json"
    map_module.save_json(final_mapping, mapping_json_path)
    console.print(f"\n  [green]OK[/green] Mapeo guardado: {mapping_json_path.name}")

    if excel:
        mapping_xlsx_path = out_path.parent / f"{out_path.stem}_mapeo.xlsx"
        map_module.save_excel(final_mapping, mapping_xlsx_path)
        console.print(f"  [green]OK[/green] Excel guardado: {mapping_xlsx_path.name}")

    # 8. Generate anonymized document
    with console.status("Generando documento anonimizado..."):
        if document.suffix.lower() == ".docx":
            replacer.anonymize_docx(document, out_path, final_mapping, modes)
        else:
            replacer.anonymize_pdf(document, out_path, final_mapping, modes)

    console.print(f"\n[bold green]Listo:[/bold green] {out_path}\n")


@app.command()
def detect(
    document: Path = typer.Argument(..., help="Ruta al documento .docx o .pdf"),
    config: Optional[Path] = typer.Option(None, "--config", "-c"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
):
    """Solo detecta entidades sin anonimizar."""
    import json
    from anonymizer import config as cfg_module
    from anonymizer.detectors import detector

    extract = _get_extractor(document)
    with console.status("Extrayendo y detectando..."):
        from anonymizer import known_entities as ke_module
        known = ke_module.load()
        doc = extract(document)
        custom_patterns = cfg_module.load_custom_patterns(config)
        entities = detector.detect_all(doc, custom_patterns, known_entities=known)

    console.print(f"\n[bold]{len(entities)} entidades detectadas:[/bold]\n")
    for ent in entities:
        console.print(
            f"  [magenta]{ent.entity_type.value}[/magenta]: "
            f"[white]\"{ent.text}\"[/white] [dim]({ent.source})[/dim]"
        )

    if output:
        suffix = output.suffix.lower()
        if suffix == ".xlsx":
            from anonymizer import mapping as map_module
            from anonymizer import known_entities as ke_module
            from anonymizer import matcher as mat_module
            
            known = ke_module.load()
            
            seen_texts = set()
            unique_entities = []
            for e in entities:
                ent_key = (e.text, e.entity_type)
                if ent_key not in seen_texts:
                    seen_texts.add(ent_key)
                    unique_entities.append(e)

            detected_texts = [e.text for e in unique_entities]
            db_matches, unmatched_texts = mat_module.match_against_db(detected_texts, known, threshold=85.0)
            
            db_matches_dict = {m.detected_text: m for m in db_matches}
            
            data_rows = []
            for e in unique_entities:
                if e.text in db_matches_dict:
                    match_res = db_matches_dict[e.text]
                    origen = "DB"
                    pseudonimo = match_res.known.pseudonym
                    accion = "s"
                else:
                    origen = str(e.source).upper()
                    pseudonimo = ""
                    accion = "s" if origen == "REGEX" else ""
                    
                data_rows.append({
                    "original": e.text,
                    "tipo": e.entity_type.value,
                    "pseudonimo": pseudonimo,
                    "accion": accion,
                    "origen": origen
                })
                
            map_module.save_extended_excel(data_rows, output)
            console.print(f"\n[green]OK[/green] Excel interactivo guardado en {output}")
        else:
            data = [{"text": e.text, "type": e.entity_type.value, "source": e.source} for e in entities]
            with open(output, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            console.print(f"\n[green]OK[/green] JSON guardado en {output}")


@app.command()
def apply(
    document: Path = typer.Argument(..., help="Ruta al documento .docx o .pdf"),
    mapping_file: Path = typer.Argument(..., help="Tabla de mapeo (.json o .xlsx)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
):
    """Aplica una tabla de mapeo existente sin revision interactiva."""
    from anonymizer import mapping as map_module, replacer

    suffix = mapping_file.suffix.lower()
    mapping = map_module.load_excel(mapping_file) if suffix == ".xlsx" else map_module.load_json(mapping_file)

    out_path = _output_path(document, output)
    with console.status("Aplicando mapeo..."):
        if document.suffix.lower() == ".docx":
            replacer.anonymize_docx(document, out_path, mapping)
        else:
            replacer.anonymize_pdf(document, out_path, mapping)

    console.print(f"[bold green]OK[/bold green] {out_path}")


@app.command()
def init_config(
    path: Optional[Path] = typer.Option(None, "--path", "-p"),
):
    """Crea un archivo de ejemplo de patrones custom."""
    from anonymizer.config import create_default_config
    config_path = create_default_config(path)
    console.print(f"[green]OK[/green] Config creada en: {config_path}")


# ── DB COMMANDS ───────────────────────────────────────────────────────────────

@db_app.command("list")
def db_list():
    """Muestra todas las entidades en la base de datos."""
    from anonymizer import known_entities as ke_module
    entities = ke_module.load()
    if not entities:
        console.print("[yellow]La base de datos esta vacia.[/yellow]")
        console.print("Usa [bold]anonymize db add[/bold] para agregar entidades.")
        return

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Original", style="white")
    table.add_column("Pseudonimo", style="green")
    table.add_column("Tipo", style="magenta")
    table.add_column("Alias", style="dim")

    for e in sorted(entities, key=lambda x: x.entity_type):
        table.add_row(
            e.original,
            e.pseudonym,
            e.entity_type,
            ", ".join(e.aliases) if e.aliases else "-",
        )

    console.print(f"\n[bold]{len(entities)} entidades en la base de datos:[/bold]\n")
    console.print(table)


@db_app.command("add")
def db_add(
    original: str = typer.Argument(..., help="Texto original a detectar"),
    pseudonym: str = typer.Argument(..., help="Pseudonimo de reemplazo"),
    entity_type: str = typer.Option("PERSONA", "--type", "-t",
                                     help="Tipo: PERSONA, ORGANIZACION, LUGAR, etc."),
    aliases: Optional[str] = typer.Option(None, "--aliases", "-a",
                                           help="Alias separados por coma (ej: 'S. Clasen,Clasen')"),
    match_mode: str = typer.Option("palabra", "--mode", "-M",
                                    help="Modo de busqueda: 'palabra' (bordes de palabra) o 'substring' (dentro de cualquier texto)"),
):
    """Agrega una entidad a la base de datos."""
    from anonymizer import known_entities as ke_module
    if match_mode not in ("palabra", "substring"):
        console.print(f"[red]Modo invalido: '{match_mode}'. Usa 'palabra' o 'substring'.[/red]")
        raise typer.Exit(1)
    alias_list = [a.strip() for a in aliases.split(",")] if aliases else []
    entity = ke_module.KnownEntity(
        original=original,
        pseudonym=pseudonym,
        entity_type=entity_type,
        aliases=alias_list,
        match_mode=match_mode,
    )
    ke_module.add(entity)
    console.print(f"[green]OK[/green] \"{original}\" -> \"{pseudonym}\" guardado [dim](modo: {match_mode})[/dim]")


@db_app.command("remove")
def db_remove(
    original: str = typer.Argument(..., help="Texto original a eliminar"),
):
    """Elimina una entidad de la base de datos."""
    from anonymizer import known_entities as ke_module
    if ke_module.remove(original):
        console.print(f"[green]OK[/green] \"{original}\" eliminado")
    else:
        console.print(f"[yellow]No encontrado:[/yellow] \"{original}\"")


@db_app.command("export")
def db_export(
    output: Optional[Path] = typer.Option(None, "--output", "-o",
                                           help="Ruta del Excel de salida. Por defecto: ~/.doc-anonymizer/known_entities.xlsx"),
):
    """Exporta la base de datos a Excel para edicion manual."""
    from anonymizer import known_entities as ke_module
    excel_path = output or ke_module.DB_PATH.with_suffix(".xlsx")
    count = ke_module.to_excel(excel_path)
    console.print(f"[green]OK[/green] {count} entidades exportadas a: {excel_path}")
    console.print("[dim]Edita el archivo en Excel y luego ejecuta:[/dim]")
    console.print(f"[bold]  anonymize db import \"{excel_path}\"[/bold]")


@db_app.command("import")
def db_import(
    source_file: Path = typer.Argument(..., help="Archivo .xlsx o .json a importar"),
    entity_type: str = typer.Option("PERSONALIZADO", "--type", "-t",
                                     help="Tipo por defecto para entradas sin tipo (solo JSON)"),
):
    """Importa entidades desde Excel (.xlsx) o desde un mapeo JSON."""
    from anonymizer import known_entities as ke_module, mapping as map_module

    suffix = source_file.suffix.lower()

    if suffix == ".xlsx":
        updated, added = ke_module.from_excel(source_file)
        console.print(f"[green]OK[/green] {added} entidades nuevas, {updated} actualizadas desde {source_file.name}")
    elif suffix == ".json":
        # Detect if it's a DB export (list) or a mapping dict
        import json
        with open(source_file, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            # Full DB export — load directly
            entities = [ke_module.KnownEntity.from_dict(e) for e in data]
            existing = {e.original for e in ke_module.load()}
            new = [e for e in entities if e.original not in existing]
            all_entities = ke_module.load() + new
            ke_module.save(all_entities)
            console.print(f"[green]OK[/green] {len(new)} entidades nuevas importadas desde {source_file.name}")
        else:
            # Simple mapping dict {"original": "pseudonym"}
            added = ke_module.import_from_mapping(data, entity_type)
            console.print(f"[green]OK[/green] {added} entidades importadas desde {source_file.name}")
    else:
        console.print(f"[red]Formato no soportado: {suffix}. Usa .xlsx o .json[/red]")
        raise typer.Exit(1)


@db_app.command("alias")
def db_alias(
    original: str = typer.Argument(..., help="Entidad existente en la DB"),
    alias: str = typer.Argument(..., help="Nuevo alias a agregar"),
):
    """Agrega un alias a una entidad existente."""
    from anonymizer import known_entities as ke_module
    entities = ke_module.load()
    for e in entities:
        if e.original == original:
            if alias not in e.aliases:
                e.aliases.append(alias)
            ke_module.save(entities)
            console.print(f"[green]OK[/green] Alias \"{alias}\" agregado a \"{original}\"")
            return
    console.print(f"[yellow]No encontrado:[/yellow] \"{original}\"")


if __name__ == "__main__":
    app()
