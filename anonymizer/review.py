from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from anonymizer.models import Entity, EntityType
from anonymizer.matcher import MatchResult

console = Console()


def review_known_matches(
    matches: list[MatchResult],
) -> tuple[dict[str, str], list[MatchResult]]:
    """
    Show pre-matched entities to the user.
    - Exact matches: auto-approved, shown as a summary table.
    - Fuzzy matches: shown one by one for confirmation.

    Returns (approved_mapping, rejected_matches)
    """
    if not matches:
        return {}, []

    exact = [m for m in matches if m.is_exact]
    fuzzy = [m for m in matches if not m.is_exact]

    approved: dict[str, str] = {}

    # Exact matches — show table and auto-approve
    if exact:
        console.print(
            f"\n[bold green]{len(exact)} entidades reconocidas automaticamente "
            f"(base de datos):[/bold green]\n"
        )
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
        table.add_column("Encontrado en doc", style="white")
        table.add_column("Pseudonimo", style="cyan")
        table.add_column("Tipo", style="magenta")
        for m in exact:
            table.add_row(m.detected_text, m.known.pseudonym, m.known.entity_type)
        console.print(table)
        for m in exact:
            approved[m.detected_text] = m.known.pseudonym

    # Fuzzy matches — confirm one by one
    if fuzzy:
        console.print(
            f"\n[bold yellow]{len(fuzzy)} coincidencias aproximadas — confirma cada una:[/bold yellow]\n"
        )
        for m in fuzzy:
            console.print(
                f"  [white]\"{m.detected_text}\"[/white] "
                f"[dim]~{m.score:.0f}%[/dim] "
                f"-> [cyan]\"{m.known.original}\"[/cyan] "
                f"= [green]\"{m.known.pseudonym}\"[/green]"
            )
            choice = Prompt.ask(
                "  [bold]Usar este pseudonimo?[/bold] [green]S[/green]i / [red]N[/red]o / [yellow]E[/yellow]ditar",
                choices=["s", "n", "e", "S", "N", "E"],
                default="s",
            ).lower()

            if choice == "s":
                approved[m.detected_text] = m.known.pseudonym
            elif choice == "e":
                pseudo = Prompt.ask("  Pseudonimo", default=m.known.pseudonym)
                approved[m.detected_text] = pseudo
            # "n" -> skip, goes to unmatched review

    return approved, [m for m in fuzzy if m.detected_text not in approved]


def review_entities(entities: list[Entity]) -> list[Entity]:
    """
    Interactive CLI review for unknown entities.
    Deduplicates by text — asks once per unique text, applies decision to all occurrences.
    Returns the confirmed list of entities to anonymize.
    """
    if not entities:
        return []

    # Deduplicate: one representative entity per unique text, track all occurrences
    seen: dict[str, Entity] = {}
    for e in entities:
        if e.text not in seen:
            seen[e.text] = e

    unique = list(seen.values())
    total_unique = len(unique)
    skipped = len(entities) - total_unique
    msg = f"\n[bold cyan]{total_unique} entidades unicas para revisar[/bold cyan]"
    if skipped:
        msg += f" [dim]({skipped} duplicadas omitidas)[/dim]"
    console.print(msg + "\n")

    confirmed: list[Entity] = []

    for i, entity in enumerate(unique):
        _print_entity_row(i + 1, total_unique, entity)

        # New entities (NER, Regex, Manual) require explicit approval
        default = "n"
        choice = Prompt.ask(
            "  [bold]Que hacer?[/bold] [green]S[/green]i / [red]N[/red]o / [yellow]E[/yellow]ditar",
            choices=["s", "n", "e", "S", "N", "E"],
            default=default,
        ).lower()

        if choice == "s":
            confirmed.append(entity)
        elif choice == "e":
            new_text = Prompt.ask("  Nuevo texto para reemplazar", default=entity.text)
            entity.text = new_text
            confirmed.append(entity)

    # Manual additions
    console.print()
    add_choice = Prompt.ask(
        "[bold]Agregar entidades manualmente?[/bold] [green]S[/green]i / [red]N[/red]o",
        choices=["s", "n", "S", "N"],
        default="n",
    ).lower()
    if add_choice == "s":
        confirmed.extend(_add_manual_entities())

    _print_summary(confirmed)
    return confirmed


def _print_entity_row(idx: int, total: int, entity: Entity):
    console.print(
        f"  [dim][{idx}/{total}][/dim] "
        f"[bold magenta]{entity.entity_type.value}[/bold magenta]: "
        f"[bold white]\"{entity.text}\"[/bold white] "
        f"[dim](fuente: {entity.source})[/dim]"
    )


def _add_manual_entities() -> list[Entity]:
    manual = []
    type_names = [e.value for e in EntityType]

    while True:
        text = Prompt.ask("  Texto de la entidad (vacio para terminar)", default="")
        if not text:
            break

        console.print("  Tipos disponibles:")
        for i, name in enumerate(type_names):
            console.print(f"    [cyan]{i+1}[/cyan]. {name}")

        idx_str = Prompt.ask("  Tipo (numero)", default="1")
        try:
            etype = list(EntityType)[int(idx_str) - 1]
        except (ValueError, IndexError):
            etype = EntityType.CUSTOM

        manual.append(Entity(
            text=text, entity_type=etype, start=-1, end=-1, source="manual",
        ))

    return manual


def _print_summary(confirmed: list[Entity]):
    if not confirmed:
        console.print("\n[yellow]Sin entidades nuevas seleccionadas.[/yellow]")
        return
    console.print(f"\n[bold green]{len(confirmed)} entidades nuevas para pseudonimizar:[/bold green]\n")
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("Tipo", style="magenta")
    table.add_column("Texto original", style="white")
    for ent in confirmed:
        table.add_row(ent.entity_type.value, ent.text)
    console.print(table)
