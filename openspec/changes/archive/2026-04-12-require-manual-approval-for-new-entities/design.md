## Context

The current user feedback indicates that auto-approving (setting `Accion="s"`) all detections is too aggressive. The user wants the system to only auto-approve entities that are already verified and stored in the Known Entities Database.

## Goals / Non-Goals

**Goals:**
- New entities (from NER or Regex) must require manual approval in both GUI (Excel mapping) and CLI workflows.
- Database hits (entities already in the Master DB) should remain auto-approved to maintain efficiency.

**Non-Goals:**
- Changing the auto-pseudonym generation logic.
- Disabling the "Guardar DB" suggestion.

## Decisions

### 1. GUI Mapping Generation
In `anonymizer/gui.py`, the `_detection_thread` loop will be updated.
- **Logic:** `accion = "s" if pseudo else ""` (where `pseudo` is the result from the matcher).
- **Rationale:** If `matcher.match` returns a value, it means the entity was found in the database.

### 2. CLI Detect Command
In `anonymizer/cli.py`, the `detect` command loop will be updated similarly.
- **Logic:** `accion = "s" if origen == "DB" else ""`.

### 3. Interactive Review Logic (CLI)
In `anonymizer/review.py`, the `review_entities` function handles the defaults for unknown entities.
- **Current logic:** `default = "n" if entity.source == "ner" else "s"` (favoring Regex/Manual).
- **New logic:** `default = "n"` (or similar).
- **Rationale:** To be strictly compliant with "solo ponga 's' para los registros encontrados en la base de datos", all new entities should default to non-approval. However, the CLI interactive step requires a choice. We will set the default to "n" for all non-database entities.

## Risks / Trade-offs

- **[Risk] User Friction** → Users will have to type "s" many more times for regex matches (emails, etc.).
- **[Mitigation]** The auto-pseudonym generator still provides a value, so the user only needs to type one character to approve.
